from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize

ground_text_data = f"""
 Below is a summary of the specific technological advancements discussed in the transcript that can be featured in an SR&ED technological_advancements section:

1. Identification and Resolution of a Novel Technological Problem:
 • The project centered on overcoming a technological challenge where an off‐the‐shelf solution was deemed inadequate.
 • The team established a framework that required setting up a hypothesis, building prototypes, conducting tests, and analyzing test results to resolve this uncertainty.
 • The problem was defined by the inability to simply apply conventional methods; instead, they needed to develop a custom methodology that integrated advanced AI techniques.

2. Redesign and Integration for Case-Based Learning:
 • A key advancement was the decision to “redo” a particular component so that it could be embedded effectively within a case‑based course.
 • This redesign was necessary to incorporate generated content and learner interactions within a real-world, educational context—transforming generic responses into context-specific, case-based learning material.
 • The innovation specifically addressed the challenge of tracking learner progress in a way that had not been established previously.

3. Leveraging and Evaluating Large Language Model (LLM) Outputs:
 • The experimental phase involved integrating GPT‑4 technology to generate interactive responses.
 • There was significant work on developing prompt techniques that not only generated answers but also “rebounded” or rephrased these outputs to ensure accuracy and relevance.
 • The team innovated on testing methods to determine if the LLM responses were correct and meaningful, thereby establishing a new standard for quality assurance in AI‐driven content delivery.

4. Adoption of Sophisticated Instructional Methodologies:
 • The project drew inspiration from early adopters like Khan Academy, which integrated GPT‑4 by emphasizing the Socratic method.
 • By incorporating the Socratic method, the team advanced the technology’s ability to support self-guided learning—effectively prompting learners to work through problems and build understanding independently.
 • This approach reflected a deliberate effort to transform the raw capabilities of GPT‑4 into an educational tool that supports nuanced, inquiry‐based learning.

Together, these components demonstrate that the project overcame significant technical uncertainties by developing novel testing protocols, reengineering content integration for case-based learning, and harnessing LLM technology in innovative ways. The iterative approach combined prototyping, validation of AI outputs, and enhanced progress tracking—advancements that directly contribute to the overall technological progression claimed under SR&ED.
"""
sred_report = f"""Technological advancements achieved as a result of the project are as follows:

Development of an adaptive machine learning algorithm: The project achieved the development of a machine learning algorithm that promotes user engagement and critical thinking. This was achieved by designing a prototype that adjusts to user behavior and generates interactive content. While the results were promising, the interface presented some usability challenges, indicating the advancement was partially achieved. The knowledge gained from this advancement will be used to refine the interface in future projects.

Application of advanced encryption and blockchain technology: The project successfully utilized advanced encryption techniques combined with blockchain technology to enhance platform security. This was achieved by developing a prototype that withstood multiple rounds of security testing and simulated cyber-attacks. The prototype was able to securely handle a large amount of fragmented data, representing a significant technological advancement in platform security.

Integration of a real-time feedback system: The project achieved the integration of a real-time, interactive feedback system that effectively captured user experiences. However, some users found the system intrusive and distracting, indicating a need for further development in balancing interactivity and user comfort. The knowledge gained from this advancement will be used to refine the feedback system in future projects.

Implementation of a thorough documentation process: The project attempted to implement a thorough documentation process to verify the credibility of the development process for SR&ED. While this approach was effective in tracking project activities, determining the eligibility of these activities for SR&ED remains a challenge. The knowledge gained from this advancement will be used to improve the documentation process in future projects.

In conclusion, the project successfully achieved significant technological advancements in the areas of machine learning, encryption and blockchain technology, and real-time feedback systems. These advancements will contribute to the company's ability to deliver innovative and secure solutions in the future. The knowledge gained from the partially achieved advancements will serve as a foundation for future R&D efforts.

"""

reference_tokens = word_tokenize(ground_text_data)
hypothesis_tokens = word_tokenize(sred_report)
print( meteor_score([reference_tokens], hypothesis_tokens))