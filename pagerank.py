import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Create a dictionary for the probabilities
    probability = dict()
    
    # Initialize all pages in the dictionary with probability 0
    for key in corpus.keys():
        probability[key] = float(0)
    
    # Check if the current page has links
    if len(corpus[page]) > 0:
        # Distribute the damping factor among the links
        for value in corpus[page]:
            probability[value] = damping_factor / len(corpus[page])
        # Add the probability of jumping to any page
        for key in probability.keys():
            probability[key] += (1 - damping_factor) / len(probability.keys())
    # If there are no links, distribute equally among all pages
    else:
        for key in probability.keys():
            probability[key] += 1 / len(probability.keys())
    
    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a dictionary for pagerank
    pagerank = dict()
    # Initialize all pages in the dictionary with probability 0
    for key in corpus.keys():
        pagerank[key] = float(0)

    # Select a random page first
    page = random.choice(list(corpus.keys()))
    # Rank pages for n samples
    for _ in range(n):
        # Get the transition model probabilities for the current page
        probability = transition_model(corpus=corpus, page=page, damping_factor=damping_factor)
        # Update the PageRank values based on the probabilities
        for key in pagerank.keys():
            pagerank[key] += probability[key]
        # Choose the next page based on the current transition probabilities
        page = random.choices(population=list(probability.keys()), 
                              weights=list(probability.values()))[0]

    # Normalize pagerank values
    for key in pagerank:
        pagerank[key] = pagerank[key] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a dictionary for pagerank
    pagerank = dict()
    num_pages = len(corpus)
    # Initialize all pages in the dictionary with probability 1 / N (number of pages in the corpus)
    for key in corpus.keys():
        pagerank[key] = 1 / num_pages

    # Threshold for convergence
    threshold = 0.001
    new_pagerank = dict()
    # Rank pages based on the PageRanks of all pages that link to it
    while True:
        for key in pagerank:
            new_rank = (1 - damping_factor) / num_pages
            sum = 0
            for page, links in corpus.items():
                # If page has no links, then treat like it has links to all pages
                if not links:
                    links = corpus.keys()
                # Check if page is a link
                if key in links:
                    sum += pagerank[page] / len(links)
            new_rank += damping_factor * sum
            new_pagerank[key] = new_rank
        
        rank_change = 0
        # Copy new ranks into pagerank dict
        for key in pagerank:
            change = abs(new_pagerank[key] - pagerank[key])
            if change > rank_change:
                rank_change = change
            pagerank[key] = new_pagerank[key]

        # Check for convergence
        if rank_change <= threshold:
            break

    return pagerank


if __name__ == "__main__":
    main()