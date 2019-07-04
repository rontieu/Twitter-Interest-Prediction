Inferring Topical Interests of Twitter Users using Natural Language Processing and Temporal Network Embedding Prediction.

The purpose of this software is to parse twitter data from a preexisting SQL database.

The primary file, the "Engine.py" is run in order to fetch the desired twitter data and produce an LDAModel with the total twitter content serving as a corpus.
Due to the nature of cloud computation the software requires an existing remotely hosted SQL database. It is also recommended that it be run on a cloud computation platform.

Users looking to run this software should adjust a few variables within the code to ensure that it can be run with their dataset. First, authentication and an IP Addresss for the SQL databse must be entered.
A link to a Concept Embedding file in the bin.gz. format is also necessary to perform the Words Movers Distance required for topic-to-topic modelling.

At this stage, the initial python script "Engine.py" may be run, producing a graphical heterogenous information network graph in an output format that is acceptable for the second stage external tool, Temporal Network Embedding. A series of edgelists in .txt format.

The second step in the pipeline is executing the external library binary for temporal network embedding and link-prediction. Each generated edgelist will serve as input for the temporal network embedding program which will produce a series of output embeddings of its own.
Temporal Network Embedding can be found and installed from here; https://github.com/linhongseba/Temporal-Network-Embedding


These embeddings can be compared against n + 1 time slices network graphs using MATLAB to produce the final AUROC plots.

Additional code including step by step Jupyter notebooks for each step of the process, Googel Cloud Platofrm specific implementations and prototype code can be found at: https://github.com/trent-rand/EDP-EB05
