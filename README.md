# Benchmarking Python XML Parsing Libraries

This is a small project to understand how diferent xml parsing python libraries compare to each other.  From this it is my hope to obtain a stronger grasp on superior methods and libraries to use when proccessing large amounts of xml data.

XML parsing libararies used for this project.
* lxml
  * http://lxml.de/
* expat
  * http://docs.python.org/2/library/pyexpat.html
* re (regular expressions)
  * http://docs.python.org/2/library/re.html
* minidom
  * http://docs.python.org/2/library/xml.dom.minidom.html


In each parsing library I took into consideration speed and scalability.
For our purposes I only wrote one profiler for each library that finds an element based off its name and specific attribute value.  Future iterations should include more profiling scenarios. 

## Testing for Speed

For this I utilized one of pythons built in profilers, cProfiler, while collecting all of the results in pStat.

http://docs.python.org/2/library/profile.html

Due to this built in library it was very simple and easy to collect the time based data.

##Testing for Scalability 

For this I ran the profiler against various xml files and valued there run times for each sample.  I've included a few of these xml files in the git one of which is over 100mb. 



## What I Found

### Parsing the large xml (mega.xml) collecting 100 samples.

* lxml
  * 2.32 seconds per sample (etree)
  * 3.28 seconds per sample (xml parser)
  * 1.01 seconds per sample iter parser
* expat
  * 3.79 seconds per sample
* re (regular expressions)
  * 0.54 seconds per sample
* minidom
  * Read over 6 gigs of memory while trying to load the file and was unable to finish the first profile run.

### Parsing the small xml (books.xml) collecting 100000 samples.

* lxml
  * 0.0002 seconds per sample (etree)
  * 0.0002 seconds per sample (xml parser)
  * 0.0001 seconds per sample (iter parser)
* expat
  * 0.00021 seconds per sample
* re (regular expressions)
 * less than 0.0000 seconds per sample
* minidom
 * 0.0036 seconds per sample

## Conclusion 
Overall our regular expressions preformed the best.  However, the use of regular expressions in any xml applicaiton is considered to be bad practice.  This webpage helps explain why.

http://www.codinghorror.com/blog/2009/11/parsing-html-the-cthulhu-way.html

Next we can note that when parsing the small xml file the diferences between each library was negligible. However when we started to scale with a larger xml file the lxml iter parser had the fastest average.
Expat was also a close contender to the lxml libraries but had some flaws.  Some of these flaws included the inability to abort parsing when the expected results were found.
We also had issues with minidom because it was unable to run the 100 megabyte file.  When ever the library loaded the file into memory it became bloated and unable to finish the first test.  It took up 6 gigs of memory before I had to kill it.
Overall most of the lxml libraries preformed well and I was satisfied with the iter parsing's simplicity, scaling, and speed.

