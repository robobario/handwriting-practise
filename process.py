import os
import sys
import json
import shutil
directory = sys.argv[1]
outdir = sys.argv[2]
uid = int(sys.argv[3])
gid = int(sys.argv[4])

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

def process(dir, subpath, config):
  outsubdir = os.path.join(outdir, subpath)
  if not os.path.exists(outsubdir):
    os.makedirs(outsubdir)
  for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    if os.path.isfile(f):
        out_pdf_file = os.path.join(filename + ".pdf")
        target_file = os.path.join(outsubdir, out_pdf_file)
        if os.path.isfile(target_file):
           print("skipping " + f + " as pdf exists already in out dir")
           break
        with open(f) as guts:
           body = guts.read().strip()
        template = templates[config["template"]]
        template = template.replace("%%BODY_GO_HERE%%", body)
        for key, value in config["parameters"].items():
            template = template.replace(key, value)
        out_tex_file = os.path.join(outsubdir, filename + ".tex")
        with open(out_tex_file, "w") as out:
           out.write(template)
        os.system('/root/bin/xelatex ' + out_tex_file)
           
        shutil.move(out_pdf_file, target_file)
        os.remove(out_tex_file)
    if os.path.isdir(f):
        process(os.path.join(dir, filename), os.path.join(subpath, filename), config)

for key, sample in config["samples"].items():
  subdir = os.path.join(directory, sample["dir"])
  outsubdir = os.path.join(outdir, key)
  process(subdir, key, sample)
  chown(outdir, uid, gid)
