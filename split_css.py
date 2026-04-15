import os

with open("style/style.backup.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

def get_lines(start_line_1_based, end_line_1_based):
    return lines[start_line_1_based - 1 : end_line_1_based]

mapping = {
    "base/typography": [],
    "base/variables": [],
    "base/reset": [],
    "layout/container": [],
    "layout/grid": [],
    "components/navbar": [],
    "components/buttons": [],
    "components/forms": [],
    "pages/resume-builder": [],
    "pages/ats": []
}

mapping["base/typography"].extend(get_lines(1, 3))
mapping["components/navbar"].extend(get_lines(4, 75))
mapping["base/variables"].extend(get_lines(77, 99))
mapping["base/reset"].extend(get_lines(101, 114))
mapping["layout/container"].extend(get_lines(116, 123))
mapping["layout/container"].extend(get_lines(125, 140))
mapping["components/buttons"].extend(get_lines(142, 166))
mapping["components/forms"].extend(get_lines(168, 254))
mapping["components/forms"].extend(get_lines(256, 280))
mapping["components/forms"].extend(get_lines(282, 292))
mapping["pages/ats"].extend(get_lines(294, 309))
mapping["pages/ats"].extend(get_lines(311, 355))
mapping["base/typography"].extend(get_lines(357, 368))
mapping["components/forms"].extend(get_lines(370, 373))
mapping["layout/container"].extend(get_lines(375, 381))
mapping["pages/ats"].extend(get_lines(383, 386))
mapping["layout/container"].extend(get_lines(388, 403))
mapping["pages/resume-builder"].extend(get_lines(405, 417))
mapping["pages/ats"].extend(get_lines(419, 432))
mapping["pages/resume-builder"].extend(get_lines(434, 462))
mapping["base/reset"].extend(get_lines(464, 481))
mapping["base/reset"].extend(get_lines(483, 497))
mapping["pages/resume-builder"].extend(get_lines(499, 517))
mapping["pages/resume-builder"].extend(get_lines(519, 528))
mapping["pages/resume-builder"].extend(get_lines(530, 538))
mapping["layout/container"].extend(get_lines(540, 558))
mapping["pages/resume-builder"].extend(get_lines(560, 619))
mapping["pages/resume-builder"].extend(get_lines(621, 642))
mapping["components/buttons"].extend(get_lines(644, 679))
mapping["components/forms"].extend(get_lines(681, 725))
mapping["pages/resume-builder"].extend(get_lines(727, 751))

# 754 is @media (max-width: 768px) {
def inject_media(file_key, start, end, query="@media (max-width: 768px) {\n"):
    mapping[file_key].append(query)
    mapping[file_key].extend(get_lines(start, end))
    mapping[file_key].append("}\n")

inject_media("layout/container", 755, 759) # .main
inject_media("base/typography", 760, 772) # headers
inject_media("components/buttons", 773, 778) # buttons
inject_media("layout/container", 779, 783) # .stCard
inject_media("layout/grid", 784, 786) # .feature-grid
inject_media("pages/ats", 787, 799) # metrics
inject_media("components/forms", 800, 813) # form
inject_media("pages/resume-builder", 814, 818) # skill
inject_media("pages/resume-builder", 819, 844) # about
inject_media("pages/ats", 845, 876) # analytics
inject_media("pages/resume-builder", 877, 881) # job role
inject_media("pages/resume-builder", 882, 893) # course card

# 896 is @media (max-width: 480px) {
q2 = "@media (max-width: 480px) {\n"
inject_media("layout/container", 897, 901, q2)
inject_media("base/typography", 902, 913, q2)
inject_media("components/buttons", 914, 918, q2)
inject_media("pages/resume-builder", 919, 921, q2)

mapping["layout/container"].extend(get_lines(924, 970))
mapping["layout/grid"].extend(get_lines(972, 991))
mapping["layout/container"].extend(get_lines(994, 1006))
mapping["pages/resume-builder"].extend(get_lines(1008, 1014))
mapping["components/navbar"].extend(get_lines(1016, 1029))

for k, v in mapping.items():
    folder, name = k.split('/')
    with open(f"styles/{folder}/_{name}.scss", "w", encoding="utf-8") as f:
        f.writelines(v)
        f.write("\n")
        f.write("\n")

print("done script 2")
