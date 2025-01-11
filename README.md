# Capstone Description

## Title: GenAI in Support of Wargaming

## Description

Creating believable, realistic, and immersive scenarios in support of wargaming objectives
requires significant time and subject matter expertise. This capstone project proposes developing a
software system that leverages Large Language Models (LLMs) to automate the creation of critical wargaming
artifacts, such as "Road to War" briefs, concepts of operations, intelligence summaries, operational plans,
and operations orders. By utilizing an LLM system capable of generating detailed, context-specific
scenarios and associated products, this project aims to greatly accelerate the wargaming process,
potentially enhance the quality of the generated outputs, and reduce the need for extensive human resources.
The project may explore LLM techniques such as Retrieval-Augmented Generation (RAG), fine-tuning, and
prompt engineering, while also developing a user-friendly interface and ensuring real-time adaptability
based on user feedback. The final product will serve as a proof of concept, demonstrating how LLMs can
be harnessed to enhance and expedite the wargaming process.

## Group Members

[Peter Asjes](mailto:m250228@usna.edu)

[William Robinson](mailto:m255334@usna.edu)

[Henry Frye](mailto:m251854@usna.edu)

[Caleb Koutrakos](mailto:m253300@usna.edu)

[Robert Ziman](mailto:m257074@usna.edu)

## POC

[LtCol Scotty Black](mailto:scotty.black@nps.edu )

## Running the project

The project is inside of a docker container that inside of a Docker containers that has all of the necessary Python packages installed. The build.sh script runs the necessary `docker build` command to create an image called *capstone*.

```bash
$ ./build.sh
```

**It will take around 10 minutes for the build to complete.**

The image can be used to create a container to run the program using the following command:

```bash
$ ./run.sh
```

## Meeting/Presentation Schedule

### Morning

Jan 23 Meeting

Jan 30 PRESENTATION

Feb 13 Meeting

Mar  6 Meeting

Mar 18 PRESENTATION

Apr  3 Meeting

### Afternoon

Jan 14 Meeting

Feb  4 Meeting

Feb 18 PRESENTATION

Feb 25 Meeting

Mar 25 Meeting

Apr 15 Meeting

Apr 17 PRESENTATION

## First Steps

- Create a small LLM that can create 5 paragraph orders.
- Nothing has really been done in this field yet, so we can pretty much do anything.
- Take a look at the wargaming documents and the wargaming plans.

## Poster

![Capstone Poster](./proposal/USNA%20Capstone%20Posterv2.png)
