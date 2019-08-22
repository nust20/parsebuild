import xml.etree.ElementTree as ET
import argparse
import os

def parse_line(parent, line, tag, tail):
	if line.isspace():
		return
	
	s = line.strip().partition("=")
	
	if s[0].startswith('#'):
		return
	
	if s[2] != "y" :
		return
	
	e = ET.SubElement(parent, tag)
	e.tail = tail
	e.set("id", s[0])	
	e.set("value", "1")
	return


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("configfile", help="Enter the kernel .config file to generate sourceinsight conditions")
	parser.add_argument("-o", "--output", help="output file name, default \"config.conditions.xml\"", default="config.conditions.xml")
	args = parser.parse_args()
	
	if not os.path.exists(args.configfile):
		print("kernel config file didn't exist!!!")
		return
	root = ET.Element("SourceInsightParseConditions")
	root.set("AppVer", "4.00.0084");
	root.set("AppVerMinReader", "4.00.0019")
	root.text = "\n\t"
	
	conditions = ET.SubElement(root, "ParseConditions")
	conditions.text = "\n\t\t"
	conditions.tail = "\n"

	defines = ET.SubElement(conditions, "Defines")
	defines.text = "\n\t\t\t"
	defines.tail = "\n\t"
	
	fp = open(args.configfile)
	
	for line in fp:
		parse_line(defines, line, "define", "\n\t\t\t")
	fp.close()
	
	tree = ET.ElementTree(root)
	tree.write(args.output)
	
	return
	
if __name__ == "__main__":
	main()