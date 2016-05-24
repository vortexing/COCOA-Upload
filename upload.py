#!/usr/bin/env python

import pandas as pd 
import synapseclient
import argparse
import os
from synapseclient import File

def upload(args):
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
		#parentId = "syn6038915"
		##vv testing vvv
		parentId = "syn6117215"
		pipeline = ["syn6038930","syn6038917"]
	elif args.dataType == "exome":
		parentId = "syn6115597"
	else:
		raise ValueError("dataType needs to be rnaseq/dnaseq/snparray/exparray/exome")
	if args.synapse_user is not None:
		syn = synapseclient.login(args.synapse_user,args.password,rememberMe=True)
	else:
		syn = synapseclient.login()
	listfiles = os.listdir(args.dir)
	annots = pd.read_csv(args.annotation)
	annots['synapseId'] = ''
	for i in listfiles:
		index = annots['Processed File Name'] == i
		temp = annots[index]
		if len(temp) != 0:
			fileEnt = File(os.path.join(args.dir,i),parent=parentId)
			del temp['Processed File Name']
			del temp['synapseId']
			#Take all the annotations and turn them into dictionary
			fileEnt.annotations = temp.to_dict('index').values()[0]
			fileEnt = syn.store(fileEnt,used = pipeline)
			annots['synapseId'][index] = fileEnt.id
	annots.to_csv(args.annotation,index=False)


#Parse args
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Upload for COCOA')

	parser.add_argument("--synapse_user", help="Synapse UserName", default=None)
	parser.add_argument("--password", help="Synapse password", default=None)
	parser.add_argument('--dir','-i',metavar='/path/to/data', type=str, required=True,
						help='Directory containing all the files')
	parser.add_argument('--annotation','-a',metavar='annotation.csv', type=str, required=True,
						help='Annotations containing mapping between sampleId and filepath along with all the annotations')
	parser.add_argument('--dataType','-d',metavar='rnaseq', type=str, required=True,
						help='Choose between rnaseq/dnaseq/snparray/exparray/exome')
	args = parser.parse_args()

	upload(args)
	