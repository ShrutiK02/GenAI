**Part 1: How to build an AI that can answer questions about your website
**Currently to reduce the crawl time I limited the code to crawl only 10 links. Feel free to remove below count and limit variables.
~~
 count = 0
    limit = 10
    # While the queue is not empty, continue crawling
    while queue and count <= limit:

        # Get the next URL from the queue
        url = queue.pop()
        count += 1
        print(url) # for debugging and to see the progress
~~
