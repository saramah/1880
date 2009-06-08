include("fileio.js")

LOWER_BOUND_DISTRICT = 586
UPPER_BOUND_DISTRICT = 588
REL_TO_HEAD = "Self"

//Substitute placeholders with string values 
// @param {string} str The string containing the placeholders 
// @param {Array} arr The array of values to substitute 
// 
function substitute(str, arr) 
{ 
  var i, pattern, re, n = arr.length; 
  for (i = 0; i < n; i++) { 
    pattern = "\\{" + i + "\\}"; 
    re = new RegExp(pattern, "g"); 
    str = str.replace(re, arr[i]); 
  } 
  return str; 
} 
//construct occupations
text = read("places.txt");
var places = text.split('\n');
var pl_length = places.length;
var SEARCH_URL = ""

if (REL_TO_HEAD == "Self"){
  SEARCH_URL = "http://search.ancestrylibrary.com/cgi-bin/sse.dll?rank=0&gsfn=&gsln=&=&f5=MA&f4=Suffolk&f7=Boston&f42=Self&f8=&f15=&f27=&f21={0}&rg_81004011__date={1}&rs_81004011__date=5&_8000C002=&f28=&_80008002=&f16=&_80018002=&f6=&f11=&f10=&f22={2}&f43=&gskw=&prox=1&db=1880usfedcen&ti=5542&ti.si=0&gl=&gss=IMAGE&gst=&so=3";
} else {
  SEARCH_URL = "http://search.ancestrylibrary.com/cgi-bin/sse.dll?rank=0&gsfn=&gsln=&=&f5=MA&f4=Suffolk&f7=Boston&f42=&f8=&f15=&f27=&f21={0}&rg_81004011__date={1}&rs_81004011__date=5&_8000C002=&f28=&_80008002=&f16=&_80018002=&f6=&f11=&f10=&f22={2}&f43=&gskw=&prox=1&db=1880usfedcen&ti=5542&ti.si=0&gl=&gss=IMAGE&gst=&so=3";
}
var results = "";

for(var index = 0, place = places[index]; index < pl_length; index++, place = places[index]){   
  for(var year = 1805; year < 1880; year += 10){
    for(var district = LOWER_BOUND_DISTRICT; district <= UPPER_BOUND_DISTRICT; district++){
      go(substitute(SEARCH_URL, [place, year, district]));
      var found = find(/\d+-\d+ of (\d+)/);
      if(found != "no matches"){
        var hits = /\d\-\d+ of (\d+)/.exec(found.text);
        results += substitute("{0},{1},{2},{3}", [district, place, year, hits[1]]) + '\n';
        output(substitute("{0},{1},{2},{3}", [district, place, year, hits[1]]))
      } else {
        results += substitute("{0},{1},{2},0", [district, place, year]) + '\n';
        output(substitute("{0},{1},{2},0", [district, place, year]))
      }
      sleep(5)
    }
  }
}
write("output.csv", results);







