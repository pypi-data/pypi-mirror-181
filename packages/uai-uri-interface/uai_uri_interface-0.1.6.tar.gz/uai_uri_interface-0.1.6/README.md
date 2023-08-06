# URI Inteface

This package provides an interface for file access that is basically a subset of pathlib.Path. It is needed because we internally use a path abstraction that allows for exactly this subset of operations. So for debugging methods that take an URI as input you can put in a pathlib.Path while we internally will input our path abstraction.
