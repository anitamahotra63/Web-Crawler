cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>






""",
   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>




""",
}
#cache is a dictionary where the key is a url and value is the html content of the corresponding url, cache = {'url':'html_content',......}
 
def ordered_search(index, ranks, keyword):
    if keyword in index:
        urlist=index[keyword]
        quicksort(urlist,ranks,0,len(urlist)-1)
        #upon receiving the sorted urlist of the keyword, it returns this list, which finally get printed.
        return urlist
    else:
        return None
  
#this method sorts the urlist of a particular keyword given by the previous written function (ordered_search) according to their ranks. then functions gets returned.
def quicksort(urlist,ranks,first,last):
    if first>=last:
        return
    pivot = (first+last)/2
    pivot_element = ranks[urlist[pivot]]
    
    while first<last:
        while ranks[urlist[first]]<pivot_element:
            first=first+1
        while ranks[urlist[last]]>pivot_element:
            last=last-1
        if first<last:
            temp=urlist[first]
            urlist[first]=urlist[last]
            urlist[last]=temp
            first=first+1
            last=last-1
            
    quicksort(urlist,ranks,0,pivot-1)
    quicksort(urlist,ranks,pivot+1,last)



#it recieves a url and checks if url exists in cache, it returns the html content of the corresponding url in case.
def get_page(url):
    if url in cache:
        return cache[url]
    return ""
   

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

#this function will recieve a html content and will return the list of all the url(s)/link(s) in that content.
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

# below two functions do this: it takes the url and its corresponding html content, splits it in several words, and put these words in dictionary 'index' as key where the value of every word of the content will be the list of url(s), in which that word is appearing
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def crawl_web(seed): # returns index, graph of inlinks
    #seed contains the initial url where we start crawling
    tocrawl = [seed]    #url to crawl to
    crawled = []        #url which have been already crawled
    graph = {}          #this is a dictionary graph:{'url1':[link1,link2,..],...}, the content at url1 contains link1 and link2 and so on
    index = {}          #this is a dictionary index:{'keyword':[list of link(s)/url(s) whose content contains this keyword]}
    while tocrawl:
        page = tocrawl.pop()   #page is a url
        if page not in crawled:
            content = get_page(page)  #content contains the html content of url, page
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks) # gives us the remaining links to crawl leavind behind the duplicates
            crawled.append(page)
    return index, graph

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks


index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)

print ordered_search(index, ranks, 'Hummus')


print ordered_search(index, ranks, 'the')

print ordered_search(index, ranks, 'babaganoush')

