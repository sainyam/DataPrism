import glob
import os

results = glob.glob('./*SIGMOD*/**/grptest.txt', recursive=True)
results += glob.glob('./*SIGMOD*/**/dp.txt', recursive=True)
results += glob.glob('./*SIGMOD*/**/*pipeline_transform*', recursive=True)
results += glob.glob('./*SIGMOD*/**/anchors.txt', recursive=True)


results = glob.glob('./Examples/**/grptest.txt', recursive=True)
results += glob.glob('./Examples/**/dp.txt', recursive=True)
results += glob.glob('./Examples/**/*pipeline_transform*', recursive=True)
results += glob.glob('./Examples**/anchors.txt', recursive=True)


for f in results:
	os.remove(f)