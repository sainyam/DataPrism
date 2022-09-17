import glob
import os

results = glob.glob('./*SIGMOD*/**/grptest.txt', recursive=True)
results += glob.glob('./*SIGMOD*/**/dp.txt', recursive=True)
results += glob.glob('./*SIGMOD*/**/*pipeline_transform*', recursive=True)
results += glob.glob('./*SIGMOD*/**/anchors.txt', recursive=True)


for f in results:
	os.remove(f)