# Benchmarking Python XML Parsing Libraries

This is a small project to understand how diferent xml parsing python libraries compare to each other.  From this it is my hope to obtain a stronger grasp on superior methods and libraries to use when proccessing large amounts of xml data.

List of XML parsing libararies that are profiled and compared in this project.
* lxml
  * http://lxml.de/
* expat
  * http://docs.python.org/2/library/pyexpat.html
* re (regular expressions)
  * http://docs.python.org/2/library/re.html
* minidom
  * http://docs.python.org/2/library/xml.dom.minidom.html


In each parsing library I took into consideration speed and scalability.
For our purposes I only wrote out one profiler for each library that finds a tag based off it's name and specific attribute value.  Future iterations should include more profiling scenarios. 

## Testing for Speed

For this I utilized one of pythons built in profilers cProfiler while collecting all of the results in pStat.

http://docs.python.org/2/library/profile.html

Due to this built in library it was very simple and easy to collect the time based data.

##Testing for Scalability 

For this I ran the profiler against various xml files and valued there run times for each sample.  I've included a few of these xml files in the git one of which is over 100mb. 



## What I Found

### Parsing the large 100 megabyte file.

* lxml
  * 2.32 seconds per sample (etree)
  * 3.28 seconds per sample (xml parser)
  * 1.01 seconds per sample iter parser
* expat
  * 3.79 seconds per sample
* re (regular expressions)
  * 0.54 seconds per sample
* minidom
  * Read over 6 gigs of memory while trying to load the file.

### Parsing the small xml file.

* lxml
  * 0.0002 seconds per sample (etree)
  * 0.0002 seconds per sample (xml parser)
  * 0.0001 seconds per sample iter parser
* expat
  * 0.00021 seconds per sample
* re (regular expressions)
  * less than 0.0000 seconds per sample

## Conclusion 
It is important to see that the regular expression preformed the best however, the use of regular expression in many xml applicaitons is considered to be bad practice.

http://www.codinghorror.com/blog/2008/06/regular-expressions-now-you-have-two-problems.html

Next we can note that when parsing small xml files the diferences between each library is negligible. However when we start to scale with a larger xml file the lxml iter parser keeps a low cost. 
Overall most of the lxml libraries preformed well and would be recomended for xml parsing in python.

