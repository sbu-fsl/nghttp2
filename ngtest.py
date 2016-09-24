#!/usr/bin/python

import sys, getopt, time, mmap
from subprocess import call

# Launch nghttp server with appropriate command:
# With push:
#   nghttpd -w30 -W30 --no-tls --htdocs=/vfs0/nghttp_data/ -p/=/assets/html/1.html,/assets/html/2.html,/assets/html/3.html,/assets/html/4.html,/assets/html/5.html,/assets/html/6.html,/assets/html/7.html,/assets/html/8.html,/assets/html/9.html,/assets/js/1.js,/assets/js/2.js,/assets/js/3.js,/assets/js/4.js,/assets/js/5.js,/assets/js/6.js,/assets/js/7.js,/assets/js/8.js,/assets/js/9.js,/assets/js/10.js,/assets/js/11.js,/assets/js/12.js,/assets/js/13.js,/assets/js/14.js,/assets/js/15.js,/assets/js/16.js,/assets/js/17.js,/assets/js/18.js,/assets/js/19.js,/assets/js/20.js,/assets/js/21.js,/assets/js/22.js,/assets/js/23.js,/assets/css/1.css,/assets/css/2.css,/assets/css/3.css,/assets/css/4.css,/assets/css/5.css,/assets/css/6.css,/assets/css/7.css,/assets/img/1.jpg,/assets/img/2.jpg,/assets/img/3.jpg,/assets/img/4.jpg,/assets/img/5.jpg,/assets/img/6.jpg,/assets/img/7.jpg,/assets/img/8.jpg,/assets/img/9.jpg,/assets/img/10.jpg,/assets/img/11.jpg,/assets/img/12.jpg,/assets/img/13.jpg,/assets/img/14.jpg,/assets/img/15.jpg,/assets/img/16.jpg,/assets/img/17.jpg,/assets/img/18.jpg,/assets/img/19.jpg,/assets/img/20.jpg,/assets/img/21.jpg,/assets/img/22.jpg,/assets/img/23.jpg,/assets/img/24.jpg,/assets/img/25.jpg,/assets/img/26.jpg,/assets/img/27.jpg,/assets/img/28.jpg,/assets/img/29.jpg,/assets/img/30.jpg,/assets/img/31.jpg,/assets/img/32.jpg,/assets/img/33.jpg,/assets/img/34.jpg,/assets/img/35.jpg,/assets/img/36.jpg,/assets/img/37.jpg,/assets/img/38.jpg,/assets/img/39.jpg,/assets/img/40.jpg,/assets/img/41.jpg,/assets/img/42.jpg,/assets/img/43.jpg,/assets/img/44.jpg,/assets/img/45.jpg,/assets/img/46.jpg,/assets/img/47.jpg,/assets/img/48.jpg,/assets/img/49.jpg,/assets/img/50.jpg,/assets/img/51.jpg,/assets/img/52.jpg,/assets/img/53.jpg,/assets/img/54.jpg,/assets/img/55.jpg,/assets/img/56.jpg -v 8080
# Without push:
#   nghttpd -w30 -W30 --no-tls --htdocs=/vfs0/nghttp_data/ -v 8080


def call_nghttp_with_push(fo, fl, n):
	start_time = time.time()
	for x in xrange(n):
		call(["nghttp", "-w30", "-W30", "http://localhost:8080/"], stdout = fo, stderr = fl)
	time_taken = round(((time.time() - start_time) * 1000) / n, 2)
	print("Avg time taken for client execution: %s ms" % time_taken)
	s = mmap.mmap(fo.fileno(), 0)
	if s.find('Not Found') != -1:
		print("Found error")

def call_nghttp_without_push(fo, fl, n):
	start_time = time.time()
	for x in xrange(n):
		call(["nghttp", "-a", "-w30", "-W30", "http://localhost:8080/"], stdout = fo, stderr = fl)
	time_taken = round(((time.time() - start_time) * 1000) / n, 2)
        print("Avg time taken for client execution: %s ms" % time_taken)
	s = mmap.mmap(fo.fileno(), 0)
	if s.find('Not Found') != -1:
    		print("Found error")

def main(argv):
	use_push = 0
	# Parsing inputs
	try:
		opts, args = getopt.getopt(argv,"hpn:")
	except getopt.GetoptError:
		print("ngtest.py -p -n <no_of_execution>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ngtest.py -n <no_of_execution>")
			sys.exit()
		elif opt == '-p':
			use_push = 1
		elif opt == '-n':
			try:
				n = int(arg)
			except ValueError:
				print("an integer value is expected for n")
				sys.exit()
	# Opening output and error log files
	fo = open("out", "a+")
        fl = open("log", "a+")
	if use_push == 1:
		call_nghttp_with_push(fo, fl, n)
	else:
		call_nghttp_without_push(fo, fl, n)
        fo.close()
        fl.close()
	# End of main

if __name__ == "__main__": main(sys.argv[1:])
