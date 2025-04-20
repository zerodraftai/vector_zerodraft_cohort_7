# flake8: noqa

guideline_text = {}

guideline_text["primary"] = """ Your role is to act as a Scientific Research and Experimental Development (SR&ED) consultant, specializing in identifying and extracting technological uncertainties from provided documents, including transcripts from meetings and technical reports. Your primary task is to evaluate these documents and pinpoint potential uncertainties that could be relevant for an SR&ED application.
To guide your evaluation, you'll use the 'Six sacred SR&ED questions' (S3Q) as a criteria framework. These questions focus on the need or desire to achieve a technological goal, the limitations of current technology, conventional approaches and their shortcomings, innovative hypotheses for overcoming these limitations, methods of prototyping and testing these hypotheses, and the analysis of test results to inform further development.
Your responses should be thorough, analytical, and focused on identifying the key technological challenges and innovative approaches detailed in the documents.

Follow these guidelines:
Six sacred SR&ED questions (S3Q)
What did you want/need to do and what technological phenomenon/limitation would not let you do it?
Example: Needed the client/server request/response transaction take less than 0.1 sec. With the current technology stack (e.g., LAMP), the transaction took more than 1 sec. 
What would be the typical (known, conventional) approach to the above issue? Why did the typical approach not work for you in this case?
Example: (a) SQL query optimization; (b) multi-threading. Tried both, the transaction duration was reduced by 20%, which was insufficient (needed an order of magnitude). 
What was your hypothesis for resolving the above issue by non-conventional means?
Example: We hypothesized that the transaction duration could be reduced by caching the least dynamic part of content at the client side, caching more dynamic part of content at the server side, and retrieving from the database only the most dynamic part of content (thus reducing the time-consuming SQL calls to the database).
How did you prototype the above hypothesis?
Example: We prototyped the above approach by using the ABC caching technique at the client side, the XYZ caching technique at the server side, and by experimentally determining what content items must be cached at the client , and what – at the server. 
How did you test the above prototype?
Example: We trialed the resulting prototype in a specially established testing environment, which was equipped by the ABC and XYZ logging/benchmarking tools, and which featured a large corpus of real-life data in the database.
What were the test results (e.g., “issue resolved,” “issue partially resolved,” issue not resolved,” etc.)? Based on the test results, what was the next step (e.g., “back to the drawing board,” “extend hypothesis,” “enhance prototype,” “solved – move on,” etc.).
Example: The trial results were positive: the average duration of a unitary client/server transaction was reduced to less than 0.1 sec. However, in the course of the trials it became clear that the updates of the cached content had to be performed either manually (which would be unrealistically labor-consuming) or by a hard-coded schedule (which could negatively impact the client/server communication performance). We had to enhance the prototype by introducing a flexible mechanism for the cached content updates. [From here – a new circle of “hypothesis – prototype – test – analysis of test results”]

Each identified uncertainty should be accompanied by a detailed explanation of the context in which it was identified, including citations or references to the transcripts and documents provided. You should also provide a detailed breakdown of the uncertainty, including the following information:
1.) Technological Uncertainty
2.) Conventional Means
3.) Innovative Hypothesis (Description of a hypothesis the company formulated to resolve the uncertainty (approach, idea, assumption) can be one or more per uncertainty)
4.) Prototype (Description of a prototype that was designed and manufactured/implemented to verify the correctness of the hypothesis, can be one or more per hypothesis)
5.) Test Methodologies (Description of the prototype tests/trials  can be one or more than one per prototype )
6.) Test Results (Description of the test results (good, not good enough, not good at all, fixed one problem but created another, etc.)
7.) Context & References (transcript or document citations or references, provide information from the transcripts or documents as supporting evidence for your uncertainty)
\n\n
"""

guideline_text["thread_rubric"] = """Rubric for SRED 'Thread' Evaluation
Thread: This refers to a specific aspect or line of investigation within a larger SR&ED project. For example, a project might have multiple "threads" of research or experimental activities, each exploring different technological uncertainties or hypotheses. Typically there are 3 threads in SRED.
Evaluation of a Thread
There are 6 categories, each one ranging from level 0 5 (0 is like a fail, and 5 is A+). Typically a passing grade is a 3 but is explained in the section. The categories are:
Technological Uncertainty
Standard practice or Existing Knowledge (Conventional Means)
Hypothesis
Prototype
Test Methodology
Test Results

Technological Uncertainty:
The Technological Uncertainty refers to an unknown that cannot be resolved through standard practice or existing knowledge. A Technological Uncertainty is a challenge or problem that requires experimental development or research to solve is a problem that the team encountered while their work on the project.
Evaluation
Level 0: No Uncertainty: Existing knowledge or standard practices can easily solve the problem. No experimentation or research needed.
Level 1: Minimal Uncertainty: There's a slight uncertainty that can be resolved with minimal experimentation, relying slightly beyond existing knowledge but not requiring extensive research.
Level 2: Minor Uncertainty: Slight doubt about the outcome, but it can be resolved with minimal experimentation or reliance on existing knowledge.
Level 3: Moderate Uncertainty: Requires systematic research or experimentation. Standard practices don't directly resolve the issue, but similar problems have been solved in the past.
Level 4: Significant Uncertainty: The problem poses a substantial challenge, requiring extensive research and experimentation. Existing knowledge provides limited guidance.
Level 5: High Uncertainty: Completely novel challenge with no known solutions or precedents. Requires extensive, groundbreaking research and experimental development.

Standard practice or Existing Knowledge (Conventional Means)
Standard Practice or Existing Knowledge refers to the current level of technology and techniques that are commonly understood and widely implemented within a specific industry. It includes:
Established Techniques: Methods and processes that are well-known and regularly used by professionals in the field.
Industry Norms: The standard approaches and solutions that are typically employed to solve common problems in the industry.
Publicly Available Information: Knowledge that can be easily accessed through publications, industry conferences, academic research, or online resources.
Evaluation
Level 0: Standard practises were not explained for this uncertainty.
Level 1: Widely Known and Applied: Techniques or knowledge are commonly used in the industry; no specialized skills or information needed beyond what is typically known.
Level 2: Common Industry Practice: Standard methods or knowledge that most professionals in the field would be familiar with; routine application without need for significant adaptation.
Level 3: Some Specialization Required: Requires specific knowledge or skills not universally known in the industry, but available through specialized training or experience.
Level 4: Advanced Knowledge/Skills: Involves techniques or information that are known to a smaller group of experts; requires significant experience or advanced training in the field.
Level 5: Cutting-Edge or Novel: Represents the forefront of the industry's knowledge; might be known only in academic or highly specialized industrial circles, often requiring innovation or extensive research to understand and apply.

Hypothesis
In SR&ED, a hypothesis is a proposed explanation or prediction made as a starting point for an experiment or investigation. It's based on limited evidence as a guide for further research. The hypothesis must be testable and address the technological uncertainty you're trying to resolve. It should lead to systematic experimentation or analysis to validate or refute it, contributing to solving the technological challenge.
Evaluation
Level 0: A hypothesis could not be located.
Level 1: Basic Hypothesis: Simple, direct assumptions with minimal complexity, often addressing straightforward problems with expected outcomes.
Level 2: Developed Hypothesis: More detailed assumptions, involving some complexity, potentially addressing more than one variable or outcome.
Level 3: Complex Hypothesis: Involves multiple variables and outcomes, requiring significant understanding of the domain to formulate.
Level 4: Highly Complex Hypothesis: Highly intricate, addressing multi-faceted technological uncertainties; requires deep domain knowledge and expertise to construct.
Level 5: Groundbreaking Hypothesis: Pushes the boundaries of the field, addressing novel or unprecedented uncertainties; requires innovative thinking and extensive expertise.

Prototype
In the context of SR&ED, a prototype is a preliminary version of a product, process, or system developed to test and validate hypotheses about technological uncertainties. The prototype serves as an experimental model to:
Explore Solutions: It's used to investigate and resolve specific technological challenges that cannot be addressed through standard practice or existing knowledge. Test Functionality: Prototypes help in assessing whether the new technology or approach works as intended. Refine Design: Based on the findings from prototype testing, improvements and modifications can be made before finalizing the design. The development of a prototype in SR&ED is a crucial step in experimental development, providing tangible evidence of the R&D efforts and their contribution to resolving technological uncertainties.
Evaluation
Level 0: A prototype could not be identified. Does not demonstrate any core functionality, Fails to address primary objectives. No features.
Level 1: Basic Functionality Prototype: Demonstrates core functionality, addressing primary objectives with minimal features. Suitable for initial proof of concept.
Level 2: Intermediate Prototype: Includes more developed features, addressing broader objectives. Tests more variables or functions beyond the basic concept.
Level 3: Advanced Prototype: Exhibits complex functionality, integrating multiple systems or technologies. Used for extensive testing and refinement.
Level 4: Near-Production Prototype: Closely resembles the final product or process, with most features and functionalities fully developed and tested.
Level 5: Production-Equivalent Prototype: Virtually indistinguishable from the final product or process. Extensively tested and validated, ready for production or full-scale implementation.

Test Methodology
In SR&ED, "test methodology" refers to the systematic approach and procedures used to evaluate the hypotheses or questions arising from technological uncertainties. It includes:
Design of Experiments: How tests are structured to isolate and identify the variables affecting the problem.
Testing Procedures: Specific steps taken to conduct the tests, ensuring they are repeatable and provide reliable data.
Data Collection and Analysis: Methods used to gather and analyze data from the tests to draw meaningful conclusions.
Documentation: Recording the test process, results, and conclusions to substantiate the R&D work for SR&ED claims.
Evaluation
Level 0: No Test Methodology: Complete absence of any structured testing approach. Experiments are random, undocumented, and provide no reliable data.
Level 1: Basic Test Methodology: Simple, ad-hoc testing methods. Limited documentation and structure, providing minimal reliable data.
Level 2: Developing Test Methodology: Some structured approach is in place. Tests are somewhat systematic with basic documentation, but not fully comprehensive.
Level 3: Structured Test Methodology: Systematic approach with clear procedures and documentation. Tests are designed to provide reliable data but may lack full sophistication.
Level 4: Advanced Test Methodology: Highly systematic and detailed approach. Includes comprehensive documentation, data analysis, and refinement based on results.
Level 5: Sophisticated Test Methodology: State-of-the-art testing processes, with meticulous documentation and analysis. Fully systematic, replicable, and designed to extract in-depth insights.

Test Results
In SR&ED, "test results" refer to the data and findings obtained from conducting experiments and tests as part of the research and development process. These results are critical for several reasons:
Evaluating Hypotheses: They provide evidence on whether the hypotheses about technological uncertainties were supported or refuted.
Guiding Development: The results inform the next steps in the experimental development process, whether it's further refinement, a change in direction, or a conclusion.
Documentation and Validation: Properly recorded test results are essential for documenting the SR&ED project, demonstrating systematic investigation and justifying the claim for tax incentives.
Learning and Innovation: Regardless of whether the results are positive, negative, or inconclusive, they contribute to the overall knowledge and understanding of the field, often leading to innovation.
Evaluation
Level 0: No Test Results: Complete absence of any results, indicating no testing was conducted or results were not recorded.
Level 1: Basic Results: Limited and rudimentary results, providing minimal insights. Possibly qualitative or anecdotal without substantial data.
Level 2: Moderate Results: Some structured data obtained, but not comprehensive. Provides limited insights into the technological uncertainties.
Level 3: Structured Results: Systematic collection of data with clearer insights. Results are documented and show evidence of addressing the hypotheses.
Level 4: Detailed Results: Comprehensive and detailed data collection. Results offer significant insights and are well-documented, demonstrating clear progress or findings.
Level 5: Extensive and Sophisticated Results: High-quality, in-depth results providing deep insights. These results are thoroughly documented and analyzed, significantly contributing to resolving the technological uncertainties.
"""

guideline_text["project_guideline"] = """SR&ED Project Guidelines - Section B Project Descriptions - Technological Uncertainties

--What scientific or technological uncertainties did you attempt to overcome?--

General description of what the project was about. For example: <The main technological objective of this project was to>. In the course of the project, the following technological uncertainties were encountered:
A numbered list of uncertainties the company resolved or tried to resolve in the course of the project.Each uncertainty should state what the issue was and why that issue could not be resolved by conventional means.
At the end it should say something like: <It was unknown what means we could employ to resolve the above issue.> 
The company failed to do a. The conventional means to resolve this issue would be b. However, we couldn’t because c.
It was unknown what means we could employ to resolve the above issue.              


--What work did you perform in the tax year to overcome the scientific or technological uncertainties described?--
(the systematic investigation or search)

THE INFORMATION IS PROVIDED FROM THE LIST OF PROJECT THREADS (UNCERTAINTIES)
USE ALL THE INFORMATION FROM THE PROVIDED UNCERTAINTIES TO FILL THIS SECTION

Use the context and references from the thread as supporting evidence for the uncertainty

Numbered paragraphs corresponding with the numbered list in the Technological Uncertainties section. Each paragraph includes the following:
a) Description of a hypothesis the company formulated to resolve the uncertainty (approach, idea, assumption) can be one or more per uncertainty
b) Description of a prototype that was designed and manufactured/implemented to verify the correctness of the hypothesis, can be one or more per hypothesis
c) Description of the prototype tests/trials and their results (good, not good enough, not good at all, fixed one problem but created another, etc.) – can be one or more than one per prototype 
d) “Bottom line”: either the issue (uncertainty) was resolved, or the efforts were abandoned (failure), or the efforts will continue in the future.

Either
The project was _____________ completed.
The project will continue in the next fiscal year in order to ***
The project was abandoned

--What scientific or technological advancements did you achieve or attempt to achieve as a result of the work described?--

The the results of the project. The focus is on what the company learned to do so that it can do the same or similar thing in the future without redoing the R&D described.
As a result of this project, <Company> gained practical knowledge and experience in <whatever>. In the course of the project, the team achieved the following technological advancements:
A numbered list of technological advancements the company sought to achieve where each advancement’s number corresponds to an uncertainty number and a number of a paragraph in the Work Done section.
Each advancement must state the following: a)	what the company sought to achieve (with emphasis on “generic”, reusable solutions).b) 	how the advancement was fully or partially achieved (by what technological means) or how the company failed to achieve it """


guideline_text["project_sample_tech_1"] = """

What technological advancements were you trying to achieve? (Maximum 350 words)

Example:
The technological objective of this project was to improve data warehouse management techniques by concentrating on the compression of relational database tables. At the time this work began, numerous database compression methods were available and many of these had been commercialized in larger software applications. However, practically all of the methods relied on data being uniformly distributed and static in nature.

By contrast, the overwhelming proportion of data entering data warehouses could not be assumed to be uniformly distributed and was almost certainly dynamic in character. We assumed that conventionally available data compression methods, such as the loss-less dictionary approach, could be surpassed by developing methods that would exploit the unique properties of those data sets that were not uniformly distributed and were dynamic. A technological advancement was therefore sought in this project through the development of data compression algorithms based on an analysis of the dynamic character and non-uniform distribution of the data sets entering the data warehouse. This work generated new technological knowledge regarding:

* the discovery and use of column value frequency of initial tables rows to create a block-based compression dictionary;
* the use of a table-wide list of most frequent values for the compression dictionary;
* the restriction of query/update/refresh operations to compressed blocks rather than entire tables;
* the organization and control of compression dictionaries in the buffer cache when calls are made to uncompress multiple blocks.

The performance of the various prototypes developed in this work was benchmarked using a number of measures based on CPU utilization and data throughput for operations including parallel load, delete/update operations, full table scan, and table access by row ID. One additional outcome of this work was that the dynamic, non-uniform data compression method developed here actually provided performance improvements for data backup and recovery operations when applied to very large databases in excess of 2.5 million rows (1.3 GB) such as those encountered in data warehouses.



What work did you perform in the tax year to overcome the technological obstacles/uncertainties? (Maximum 700 words)

Example:
Following a review of available software methods and dataset characterization techniques, beginning in March 2008 the first phase of the investigations focused on the analysis of a very large data set (known to be dynamic with a non-uniform distribution) in relational database form. This analysis involved a number of investigations, using selected well-known methods in software engineering, with the aim of creating a generalized model of a data set. This also included the extraction of a number of dataset-specific conclusions regarding row and column correlations and distributions, some of which are briefly outlined above in the technological advancements section. At the end of this first phase we found that a reasonably accurate data set model could be created. This was further tested and the data set model accuracy was verified and validated against several concrete smaller-sized relational databases available to us in the data warehouse.

In the second phase, starting in May 2008, a number of compression methods were developed in prototype forms to exploit the general features of the data model. Each prototype carried a set of specific assumptions regarding how the dataset characteristics might be exploited and each was subsequently verified for integrity and then benchmarked for performance. This benchmarking was done through measures of CPU utilization and data throughput for parallel load, delete/update operations, full table scan, and table access by row ID. In direct support of this work, several test scripts were written to test the compression algorithm. Although the development of these scripts included no significant technological challenge, they were necessary to benchmark the new algorithms and determine the most appropriate solution. The benchmarking results were documented and are available for further review if requested.

The third phase was carried out in June and July 2008. Three candidate compression algorithms were modified to include an implementation of several different dynamic compression techniques for dataset additions and/or updates. Each of these again had the data integrity verified and performance benchmarked, the latter now including update/refresh-specific performance measures. In August 2008, a final prototype was selected for widespread commercial implementation ending this aspect of the experimental development.

During October 2008 the implemented prototype was used to determine whether or not an optimal data table compression-block size could be determined by both the initial data set analysis and the dynamic analysis. However, this work failed to establish that such a relationship existed and was subsequently abandoned, ending the project in November 2008.

As part of this effort the Company engaged an outside contractor for a period of two months to extend the data compression method to a wider range of common data warehouse operations in September 2008. Included in this work was an exploration into use of the implemented compression prototype for data backup and recovery operations. As the result of this work it was found out and further documented that the prototype provided measurable performance improvements when applied to very large databases in excess of 2.5 million rows (1.3 GB) such as those typically encountered in data warehouses. Subsequent investigations revealed that this was primarily due to the construction of the compression dictionary rather than the data blocks.



What technological obstacles/uncertainties did you have to overcome to achieve the technological advancements?

Example:
There were a number of specific technological obstacles that drove the systematic investigations described further.
We were looking for an appropriate methodology of modeling our dynamic, non-uniform data distribution in real data for the purposes of the compression prototypes.

There were no methodologies, techniques, or models available to us to characterize dynamic, non-uniform data. Our review of available techniques revealed in the early phase of the project that we had to undertake investigation leading to the development of a dataset model suitable to reflect in an efficient way our specific dataset characteristics. The second technological shortcoming was that we did not know and we could not find any technique or methodology related to the data compression, which would specifically deal with this data model related to dynamic, non-uniform data. We realized that if we develop a suitable model to characterize dynamic, non-uniform data then we would find no established techniques to be applied to the data compression aspect that would effectively and efficiently exploit the general features of this abstract data model previously mentioned.
The effectiveness of each feature had to be verified in terms of data integrity and benchmark performance comparisons. Once a series of candidate compression algorithms became available the subsequent technical shortcomings were associated with the possibility of implementing a dynamic compression technique for dataset additions and/or updates on a batch basis. Finally, we were planning to develop an acceptable and valid methodology of setting up some general rules related to an optimal data table compression-block size applicable to both the initial data set analysis and the dynamic analysis. We felt that such a relationship should exist and we decided to undertake an investigation to be able to prove it. We also realized that such methodology is not readily available so we would have to address this issue and develop a technique potentially leading to determining an optimal data-block size.
"""

guideline_text["candidates_guideline"] = """ Given a list of threads(uncertainties) and their evaluations, identify which threads are candidates for a SR&ED project and group them, ensure that each group of threads(uncertainties) is sufficiently strong enough for a SR&ED project, ideally no less than 3 threads per project. Return groups of threads that would make the strongest project claims with a project title, project description, and project thread ids.

"""