# Notes about responses

## response headers
When a new pin is available, the header will have `X-pin`. But if a new one is not generated, the response header does not have it.


## nextissuetime
Returns time in unix time. If that time has already passed, that means that there are 5 unaddressed issues.

```xml
<NATION id="group5">
    <NEXTISSUETIME>1668161440</NEXTISSUETIME>
</NATION>
```


## nextissue
This is the same as nextissuetime but it returns plain english
```xml
<NATION id="group5">
    <NEXTISSUE>in 1 minute</NEXTISSUE>
</NATION>
```

## issue response
Please have a look at [response_to_answered_issue](./response_to_answered_issue.xml) for full details

### rankings
Refer to [issue 30](https://github.com/fsu-fall2022-capstone/Project-Group-5/issues/30) for some more details. Ideally, if we could have images of every ranking and then make a graphic of the changes, that would be best. Similar to how it is done on the website. To grab the images, the url looks like https://www.nationstates.net/images/trophies/pizza-100.png. Having them locally is best. Manual work is needed   
Score is the new score. Change is the amount changed. And pchange is the percentage it changed.
```XML
<RANKINGS>
  <RANK id="5">
    <SCORE>35.38</SCORE>
    <CHANGE>0.03</CHANGE>
    <PCHANGE>0.084866</PCHANGE>
  </RANK>
</RANKINGS>
```

### unlocks
The banner ids are given, but not the conditions for unlock. We can display the banner as is.

### error
Same command was ran on an already done command. Here is an example of an error
```xml
<NATION id="group5">
  <ISSUE id="505" choice="3">
    <ERROR>Issue already processed!</ERROR>
  </ISSUE>
</NATION>
```

### missing examples of:
 * RECLASSIFICATIONS
 * REMOVED_POLICIES