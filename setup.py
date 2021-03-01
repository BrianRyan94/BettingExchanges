import setuptools

setuptools.setup(
    name="betfair_smarkets_simple",
    version="0.1.9",
    author="Brian Ryan",
    author_email = "brian.ryan@ucdconnect.ie",
    description="Wrappers for smarkets/betfair APIs",
    packages=['betfairwrapper','smarketswrapper'],
    url="https://github.com/BrianRyan94/BettingExchanges",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
