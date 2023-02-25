import os
import sys
import json
import shutil
directory = sys.argv[1]
outdir = sys.argv[2]
uid = int(sys.argv[3])
gid = int(sys.argv[4])
regen = sys.argv[5] == "True"

with open(os.path.join(directory, "config.json")) as f:
  config = json.load(f)

file_path = os.path.dirname(os.path.realpath(__file__))
templates = {}
template_dir = os.path.join(file_path, "templates")
for filename in os.listdir(template_dir):
  f = os.path.join(template_dir, filename)
  if os.path.isfile(f):
    with open(f) as template_file:
      templates[filename] = template_file.read()
  

def chown(path, user, group):
    try:
        for root, dirs, files in os.walk(path):
            shutil.chown(root, user, group)
            for item in dirs:
                shutil.chown(os.path.join(root, item), user, group)
            for item in files:
                shutil.chown(os.path.join(root, item), user, group)
    except OSError as e:
        raise e 

def read(path):
    with open(path) as guts:
        return guts.read()

def process(dir, subpath, config):
  outsubdir = os.path.join(outdir, subpath)
  if not os.path.exists(outsubdir):
    os.makedirs(outsubdir)
  for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    if os.path.isfile(f):
        out_pdf_file = os.path.join(filename + ".pdf")
        target_file = os.path.join(outsubdir, out_pdf_file)
        if (not regen) and os.path.isfile(target_file):
           print("skipping " + f + " as pdf exists already in out dir")
        else:
           body = read(f).strip()
           print(body)
           template = templates[config["template"]]
           template = template.replace("%%BODY%%", body)
           print(template)
           for key, value in config["parameters"].items():
              template = template.replace(key, value)
           out_tex_file = os.path.join(outsubdir, filename + ".tex")
           with open(out_tex_file, "w") as out:
              out.write(template)
           os.system('/root/bin/xelatex --halt-on-error "' + out_tex_file + '"')
           shutil.move(out_pdf_file, target_file)
           os.remove(out_tex_file)
    if os.path.isdir(f):
        process(os.path.join(dir, filename), os.path.join(subpath, filename), config)

def generate_index(path, relative_dir="/", parent=""):
  if relative_dir == "/":
    header = "NZ Handwriting Sheets"
  else:
    header = os.path.basename(path)
  current_dir_displayname = header
    
  directories = []
  files = []
  for filename in os.listdir(path):
    f = os.path.join(path, filename)
    if os.path.isfile(f):
      files.append(filename)
    elif os.path.isdir(f):
      directories.append(filename)
  files.sort()
  directories.sort()
  dir_rows = ["<tr><td><span class=\"icon-text\"><span class=\"icon\"><icon class=\"fas fa-regular fa-folder\"></icon></span><span><a href=\"./" + d + "/index.html\">"+d+"</a></span></span></td></tr>" for d in directories]
  file_rows = ["<tr><td><span class=\"icon-text\"><span class=\"icon\"><icon class=\"fas fa-regular fa-file-pdf\"></icon></span><span><a href=\"./" + f + "\">"+f+"</a></span></span></td></tr>" for f in files if f.endswith(".pdf")]
  template = templates["index_page.html"]    
  file_blob = "\n".join(file_rows)
  dir_blob= "\n".join(dir_rows)
  parent_row="<tr><td><span class=\"icon-text\"><span class=\"icon\"><icon class=\"fas fa-solid fa-chevron-up\"></icon></span><span><a href=\"../index.html\">"+parent+"</a></span></span></td></tr>"
  rows = parent_row + "\n" + dir_blob + "\n" + file_blob
  template = template.replace("%%HEADER%%", header)
  template = template.replace("%%ROWS%%", rows)
  if relative_dir != "/":
      with open(os.path.join(path, "index.html"), "w") as out:
          out.write(template)
  for dir in directories:
      generate_index(os.path.join(path, dir), os.path.join(relative_dir, dir), current_dir_displayname)
    

for key, sample in config["samples"].items():
  subdir = os.path.join(directory, sample["dir"])
  outsubdir = os.path.join(outdir, key)
  process(subdir, key, sample)
generate_index(outdir)
chown(outdir, uid, gid)
