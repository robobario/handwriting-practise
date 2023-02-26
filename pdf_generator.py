import os
import shutil

file_path = os.path.dirname(os.path.realpath(__file__))
templates = {}
template_dir = os.path.join(file_path, "templates")
for filename in os.listdir(template_dir):
    f = os.path.join(template_dir, filename)
    if os.path.isfile(f):
        with open(f) as template_file:
            templates[filename] = template_file.read()


def get_template(name):
    return templates[name]

def gen_pdf(body, config, out_dir, filename, target_file):
    template = templates[config["template"]]
    template = template.replace("%%BODY%%", body)
    for key, value in config["parameters"].items():
        template = template.replace(key, value)
    out_tex_file = os.path.join(out_dir, filename + ".tex")
    out_pdf_file = os.path.join(filename + ".pdf")
    with open(out_tex_file, "w") as out:
        out.write(template)
    os.system('/home/myuser/bin/xelatex --halt-on-error "' + out_tex_file + '"')
    shutil.move(out_pdf_file, target_file)
    os.remove(out_tex_file)
