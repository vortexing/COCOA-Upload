#!/usr/bin/env python

#import pandas as pd 
import synapseclient
import argparse
import os
from synapseclient import File

def annotate(args,syn):
	import pandas as pd
	if args.dataType == "rnaseq":
		parentId = "syn6034916"
		pipeline = ["syn6035385","syn6035389","syn6035387"]
	elif args.dataType == "dnaseq":
		parentId = "syn6034751"
		pipeline = ["syn6039277","syn6034908","syn6034910","syn6034909","syn6034913"]
	elif args.dataType == "snparray":
		parentId = "syn6038475"
		pipeline = ["syn6038932","syn6038912"]
	elif args.dataType == "exparray":
		parentId = "syn6038915"
		pipeline = ["syn6038930","syn6038917"]
	elif args.dataType == "exome":
		parentId = "syn6115597"
	else:
		raise ValueError("dataType needs to be rnaseq/dnaseq/snparray/exparray/exome")
	#listfiles = os.listdir(args.dir)
	listfiles = syn.chunkedQuery('select id, name from file where parentId == "%s"' %parentId)
	annots = pd.read_csv(args.annotation)
	annots['synapseId'] = ''
	for i in listfiles:
		index = annots['filePath'] == i['file.name']
		temp = annots[index]
		if len(temp) != 0:
			#fileEnt = File(os.path.join(args.dir,i),parent=parentId)
			fileEnt = syn.get(i['file.id'],downloadFile=False)
			del temp['filePath']
			del temp['synapseId']
			#Take all the annotations and turn them into dictionary
			fileEnt.annotations = temp.to_dict('index').values()[0]
			fileEnt = syn.store(fileEnt,used = pipeline,forceVersion=False)
			annots['synapseId'][index] = fileEnt.id
	annots.to_csv(args.annotation,index=False)


def upload(args,syn):
	if args.dataType == "rnaseq":
		parentId = "syn6034916"
		pipeline = ["syn6035385","syn6035389","syn6035387"]
		dataType = "RNASeq"
	elif args.dataType == "dnaseq":
		parentId = "syn6034751"
		pipeline = ["syn6039277","syn6034908","syn6034910","syn6034909","syn6034913"]
		dataType = "TargDNASeq"
	elif args.dataType == "snparray":
		parentId = "syn6038475"
		pipeline = ["syn6038932","syn6038912"]
		dataType = "SNParray"
	elif args.dataType == "exparray":
		parentId = "syn6038915"
		pipeline = ["syn6038930","syn6038917"]
		dataType = "expression_microarray"
	elif args.dataType == "exome":
		parentId = "syn6115597"
	else:
		raise ValueError("dataType needs to be rnaseq/dnaseq/snparray/exparray/exome")
	fileEnt = File(args.input,parent=parentId)
	fileEnt.annotations = temp.to_dict('index').values()[0]
	fileEnt.dataType = dataType
	fileEnt.sampleId = sampleId
	fileEnt = syn.store(fileEnt,used = pipeline)
	return(fileEnt.id)

def perform_main(args):
	if args.synapse_user is not None:
		syn = synapseclient.login(args.synapse_user,args.password,rememberMe=True)
	else:
		syn = synapseclient.login()
	if 'func' in args:
		try:
			args.func(args,syn)
		except Exception as ex:
			print(ex)

##Annotations need to have consistent columns
#Parse args
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Upload for COCOA')

	parser.add_argument("--synapse_user", help="Synapse UserName", default=None)
	parser.add_argument("--password", help="Synapse password", default=None)

	subparsers = parser.add_subparsers(title='commands',
		description='The following commands are available:')

	parser_upload = subparsers.add_parser('upload',
			help='Upload COCOA files')
	parser_upload.add_argument('--input','-i',metavar='/path/to/data', type=str, required=True,
						help='Directory containing all the files')
	parser_upload.add_argument('--sampleId','-s',metavar='sample123', type=str, required=True,
						help='Sample ID of specific file')
	parser_upload.add_argument('--dataType','-d',metavar='rnaseq', type=str, required=True,
						help='Choose between rnaseq/dnaseq/snparray/exparray/exome')
	parser_upload.set_defaults(func=upload)


	parser_annotate = subparsers.add_parser('annotate',
			help='Annotate COCOA files')
	#parser_annotate.add_argument('--synId',metavar='syn1234', type=str, required=True,
#						help='synapse Id of folder with entities')
	parser_annotate.add_argument('--annotation','-a',metavar='/path/to/annotations.csv', type=str, required=True,
						help='All the REDCap annotations')
	parser_annotate.add_argument('--dataType','-d',metavar='rnaseq', type=str, required=True,
						help='Choose between rnaseq/dnaseq/snparray/exparray/exome')
	parser_annotate.set_defaults(func=annotate)

	args = parser.parse_args()
	perform_main(args)
	