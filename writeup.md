# Abstract

Exemplar theory has long dominated explanations of human categorization
behavior, but a growing body of evidence reveals systematic failures
within artificial classification learning---the very domain where
exemplar models should be most successful. The current study
investigates an alternative framework based on learned regularities and
feature correlations rather than similarity to stored exemplars. This
coherence-based approach is embodied by the DIVergent Autoencoder (DIVA)
model, which learns to reconstruct category members\' features and
thereby extracts within-category correlational structure. Experiment 1
directly contrasted DIVA against the Generalized Context Model (GCM)
using category structures where the models make opposite predictions.
Computational simulations confirmed divergent predictions, and
behavioral results [strongly]{.deletion author="Kenneth Kurtz"
date="2026-01-03T03:09:00Z"} favored DIVA: subjects generalized novel
items based on learned feature correlations rather than exemplar
similarity. [we don\'t typically put numbers in the abstract, do you
think it is important to do so?]{.comment-start id="8"
author="Kenneth Kurtz" date="2026-01-03T03:05:00Z"}Quantitative model
fitting showed superior performance for DIVA (MSE = 0.006) compared to
GCM (MSE = 0.0075)[]{.comment-end id="8"}. Experiment 2 examined how
[the categorization problem]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:11:00Z"}[domain structure]{.deletion
author="Kenneth Kurtz" date="2026-01-03T03:11:00Z"} []{.insertion
author="Kenneth Kurtz" date="2026-01-03T03:11:00Z"}influences
representational strategy [by contrasting]{.deletion
author="Kenneth Kurtz" date="2026-01-03T03:12:00Z"} [by assessing
learning of]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:12:00Z"} a highly structured category
[versus]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:13:00Z"}[with]{.deletion author="Kenneth Kurtz"
date="2026-01-03T03:13:00Z"} an unstructured category. [In this
case,]{.insertion author="Kenneth Kurtz" date="2026-01-03T03:14:00Z"}
[M]{.deletion author="Kenneth Kurtz"
date="2026-01-03T03:14:00Z"}[m]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:14:00Z"}ost subjects relied on
[exemplar?]{.comment-start id="19" author="Kenneth Kurtz"
date="2026-01-03T03:15:00Z"}similarity[]{.comment-end id="19"}-based
generalization that worked across both categories, suggesting strategic
adaptation to domain-wide utility. [Additionally, in conditions
where]{.insertion author="Kenneth Kurtz" date="2026-01-03T03:16:00Z"}
[S]{.deletion author="Kenneth Kurtz"
date="2026-01-03T03:16:00Z"}[s]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:16:00Z"}ubjects [were told to]{.insertion
author="Kenneth Kurtz" date="2026-01-03T03:16:00Z"}
expect[ing]{.deletion author="Kenneth Kurtz"
date="2026-01-03T03:16:00Z"} to learn additional categories [after the
initial two-way training, learners]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:16:00Z"} were even less likely to use
structure-based strategies[--]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:17:00Z"}[,]{.deletion author="Kenneth Kurtz"
date="2026-01-03T03:17:00Z"} indicating[what do you mean
here?]{.comment-start id="28" author="Kenneth Kurtz"
date="2026-01-03T03:06:00Z"} sophisticated reasoning[]{.comment-end
id="28"} about representational effectiveness. Experiment 3 tested
whether correlation strength [what do you mean here?]{.comment-start
id="29" author="Kenneth Kurtz"
date="2026-01-03T03:18:00Z"}causally[]{.comment-end id="29"} influences
coherence-based learning but [revealed]{.insertion
author="Kenneth Kurtz" date="2026-01-03T03:18:00Z"}[found]{.deletion
author="Kenneth Kurtz" date="2026-01-03T03:18:00Z"} [may need to
explain]{.comment-start id="32" author="Kenneth Kurtz"
date="2026-01-03T03:19:00Z"}no graded []{.comment-end
id="32"}relationship. Instead, robust category idealization emerged
across conditions, with subjects systematically reclassifying training
items and rating extreme-valued novel items as more typical than
familiar exemplars. This [is it clear why this is
suggested?]{.comment-start id="33" author="Kenneth Kurtz"
date="2026-01-03T03:19:00Z"}suggests[]{.comment-end id="33"} multiple
competing representational processes rather than a single dominant
mechanism. Together, the [three]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:20:00Z"}[se]{.deletion author="Kenneth Kurtz"
date="2026-01-03T03:20:00Z"} experiments demonstrate that human
categorization involves flexible deployment of different
representational strategies depending on category structure and task
demands. Categories can be organized around stored exemplars, extracted
correlational regularities, or contrast-based ideals[--]{.insertion
author="Kenneth Kurtz" date="2026-01-03T03:20:00Z"}[,]{.deletion
author="Kenneth Kurtz" date="2026-01-03T03:20:00Z"} with different
processes competing or cooperating based on contextual factors. These
findings challenge single-mechanism theories and point toward more
adaptive [accounts]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:20:00Z"}[models]{.deletion author="Kenneth Kurtz"
date="2026-01-03T03:20:00Z"} of human concep[t formation and
generalization.]{.insertion author="Kenneth Kurtz"
date="2026-01-03T03:20:00Z"} [tual knowledge.]{.deletion
author="Kenneth Kurtz" date="2026-01-03T03:20:00Z"}

# Introduction

[seems like nosofsky 84, 86 should be here.  maybe throw in a recent
rocks paper?  and the most cited review paper by nosofsky and/or
kruschke to give some overall coverage?]{.comment-start id="43"
author="Kenneth Kurtz" date="2026-01-03T04:11:00Z"}Exemplar theory has
been positioned as the preeminent account of human categorization by
numerous empirical demonstrations of its explanatory power: good
quantitative fits to classic benchmarks (Kruschke, [1992,]{.insertion
author="Kenneth Kurtz" date="2026-01-03T04:05:00Z"} 1993; Nosofsky,
Gluck, Palmeri, McKinley, & Glauthier, 1994), accurate predictions in
the 5-4 category structure (Medin & Schaffer, 1978), accounts of shift
learning difficulty (Kruschke, 1996), the inverse base-rate effect
(Kruschke, 2001; 2003), and typicality effects (Nosofsky, 1988), among
others.[]{.comment-end id="43"}

However, a growing body of evidence reveals systematic failures of
exemplar theory within the very domain where it should be most
successful: artificial classification learning with simple perceptual
stimuli. These failures suggest that human categorization involves more
than similarity to stored exemplars, pointing instead toward
representations organized around learned regularities and [i like to
save \"structural\" for the relational cog side of what we do\... would
that be manageable?]{.comment-start id="45" author="Kenneth Kurtz"
date="2026-01-03T04:11:00Z"}structural[]{.comment-end id="45"}
coherence.

The clearest evidence comes from studies of feature correlation
learning. [i am \_so\_ on the verge of submitting \"catflip\"!  so, in
additional to the dissertation (and maybe also a cogsci proceedings?),
we can cite the paper under review here \-- ask me for the
cite]{.comment-start id="46" author="Kenneth Kurtz"
date="2026-01-03T04:17:00Z"}Conaway (2016) []{.comment-end id="46"}found
that categories with strong within-category feature correlations are
learned more easily than matched controls[,]{.deletion
author="Kenneth Kurtz" date="2026-01-03T04:17:00Z"} [with]{.insertion
author="Kenneth Kurtz" date="2026-01-03T04:17:00Z"}[even when]{.deletion
author="Kenneth Kurtz" date="2026-01-03T04:17:00Z"} between-category and
within-category similarity [are]{.deletion author="Kenneth Kurtz"
date="2026-01-03T04:18:00Z"} equated [but no global statistical
structure]{.insertion author="Kenneth Kurtz"
date="2026-01-03T04:18:00Z"}. The key insight is that similarity
structure was held constant while correlation structure varied,
[and]{.insertion author="Kenneth Kurtz"
date="2026-01-03T04:18:00Z"}[yet]{.deletion author="Kenneth Kurtz"
date="2026-01-03T04:18:00Z"} subjects were clearly sensitive to the
latter [in their learning ability]{.insertion author="Kenneth Kurtz"
date="2026-01-03T04:18:00Z"}. This suggests that learners extract and
utilize regularities in how features co-occur within
categories---information that exemplar models [might need a caveat here
about exemplar models operating on distance in \*psychological space\* 
\-- is that something we talk about in this paper as
well?]{.comment-start id="55" author="Kenneth Kurtz"
date="2026-01-03T04:21:00Z"}do not explicitly represent.[]{.comment-end
id="55"}

[can we fill this out a bit more for people who haven\'t read the
paper?  also let\'s bring up the nosofsky response paper that adds
nuance but does not refute the partial XOR result? (do you agree with
this interp?)]{.comment-start id="56" author="Kenneth Kurtz"
date="2026-01-03T04:24:00Z"}The importance of such regularities becomes
even clearer in generalization behavior. Conaway & Kurtz (2017)
presented subjects with novel items that maintained learned feature
correlations but were not necessarily similar to training
exemplars[]{.comment-end id="56"}. [let\'s be a little more precise
about the rate at which this occurred, agreed?]{.comment-start id="57"
author="Kenneth Kurtz" date="2026-01-03T04:25:00Z"}Subjects
systematically classified []{.comment-end id="57"}these items based on
whether they conformed to the extracted correlations rather than their
similarity to stored instances. This directly contradicts the core
assumption of exemplar theory that generalization reflects similarity to
remembered cases.

Even within the canonical domain of the Shepard, Hovland, & Jenkins
(1961) category structures---long considered a showcase for exemplar
models---problems have emerged. Kurtz et al. (2012) demonstrated that
the classic Type II advantage depends critically on instructional
context. When rule-based language is removed from instructions, the
advantage disappears. Crucially, ALCOVE cannot account for both the
original and revised orderings: modifications that improve fit to the
revised ordering worsen fit to the original data.

These failures are not isolated phenomena. Other challenging findings
include contrast-based ideals where extreme-valued items are judged more
typical than familiar category members (Levering & Kurtz, 2006;
Silliman, 2021) and alternating category structures that subjects can
learn and generalize despite violating similarity-based predictions
(Kurtz & Wetzel, 2021). While these phenomena may involve different
mechanisms, they collectively point to a fundamental limitation in how
exemplar models conceive of category representation---as collections of
stored instances rather than organized knowledge structures based on
extracted regularities.

The DIVergent Autoencoder (DIVA; Kurtz, 2007; [i think i also attempted
various explanatory metaphors for diva in that chapter \-- maybe see if
there\'s any you think are worthy to include here.   also, while in
london i tried to write a new clean description and came up with the
following that we could possibly work in some language from:  \
DIVA recodes inputs by projecting them into a constructed latent space
and builds a coordinated recoding-decoding circuit for each category
(optimized via auto-associative, error-corrective learning) which
responds positively to the appropriate training items. These circuits
identify known category members and generalize to novel items by
responding positively (with low reconstructive error) to inputs with a
suitable combination of within-category regularities. Each circuit is an
implicit statistical model of the category (i.e., embodied in the
weights) which can be seen as a collection of possible paths to category
membership. Each path embodies a thread of category knowledge such as:
membership is consistent with f1 is \'1\' and the conjunction of f2 and
f3 is not \'01\'. Some paths are more abstractive and account for the
membership of many examples, while others are highly specific and
account for membership of a single training item. Depending on initial
weights and hyperparameter settings, DIVA produces different variations
of its circuits and paths; providing flexibility and diversity as an
account of inductive category learning. In sum, the category
representation is not explicitly realized (as in a logical rule or
stored reference points like exemplars or prototypes) \-- it is inherent
in a discovered constellation of local, \'brain-style\' operations which
collectively embody a function that takes inputs and returns
goodness-of-fit to each category.]{.comment-start id="58"
author="Kenneth Kurtz" date="2026-01-03T04:36:00Z"}[i wrote a diva
review paper in the 2020s that i happen to like \-- let\'s put that
here!]{.comment-start id="59" author="Kenneth Kurtz"
date="2026-01-03T04:30:00Z"}2015[[]{.comment-end id="58"}]{.comment-end
id="59"}) provides an account based on learned coherence that succeeds
where exemplar models fail, particularly for phenomena involving feature
correlations and [i won\'t keep marking this, but you can do a search
for the term?]{.comment-start id="60" author="Kenneth Kurtz"
date="2026-01-03T04:27:00Z"}structural[]{.comment-end id="60"}
regularities. [should we start mentioning the commonalities DIVA has
with the tech of the gen AI revolution or is that beside the
point?]{.comment-start id="61" author="Kenneth Kurtz"
date="2026-01-03T04:29:00Z"}DIVA is a modified autoencoder
[]{.comment-end id="61"}with separate reconstruction channels for each
category. During training, the model learns to reconstruct category
members\' features from a shared hidden representation. This
architecture forces DIVA to discover within-category feature
regularities---categories with strong feature correlations produce more
accurate reconstructions and are easier to learn.

At test, items are classified based on which category channel produces
the best reconstruction. Classification depends on whether an item\'s
feature pattern matches the learned regularities of a category, not
similarity to stored exemplars. This allows DIVA to generalize based on
feature correlations and structural coherence, naturally accounting for
the correlation-based learning and generalization effects that challenge
exemplar models.

[this seems a bit short and sudden\...  i think we need to do a little
more to motivate the so-called gap \-- what do we not yet know that is
critically important and interesting to find out??]{.comment-start
id="62" author="Kenneth Kurtz" date="2026-01-03T04:40:00Z"}The present
experiments systematically test when and how coherence-based
representations (as []{.comment-end id="62"}implemented in DIVA)
outperform similarity-based accounts (as exemplified by the GCM). We
focus on category structures with strong feature correlations where
these approaches make clearly divergent predictions, allowing direct
empirical tests of their relative explanatory power. Experiment 1
provides a direct computational and behavioral test where DIVA and GCM
make opposite predictions about generalization to novel items.
Experiment 2 examines how domain structure influences the adoption of
coherence-based versus similarity-based strategies. Experiment 3
investigates the relationship between feature correlation strength and
coherence-based generalization, while also examining how idealization
processes interact with coherence-based learning.

# [i think we need an experiment-specific intro for each exp.  doesn\'t have to be long but needs to set up the question and logic.  maybe you can pull some of this out of the Design section and restrict that section to concretely detailing the set-up of IV and DV?]{.comment-start id="64" author="Kenneth Kurtz" date="2026-01-03T20:22:00Z"}Experiment 1[]{.comment-end id="64"}

## Methods

### Participants

[need to say something about sample size justification.]{.comment-start
id="67" author="Kenneth Kurtz" date="2026-01-03T20:18:00Z"}30
undergraduate students []{.comment-end id="67"}from Binghamton
University participated for partial fulfillment of a course requirement.

### Design

The experiment consisted of a two-[way]{.insertion
author="Kenneth Kurtz" date="2026-01-03T20:26:00Z"}[class]{.deletion
author="Kenneth Kurtz" date="2026-01-03T20:26:00Z"} classification task
with a[n]{.deletion author="Kenneth Kurtz" date="2026-01-03T20:27:00Z"}
[supervised]{.insertion author="Kenneth Kurtz"
date="2026-01-03T20:27:00Z"}[initial]{.deletion author="Kenneth Kurtz"
date="2026-01-03T20:27:00Z"} []{.insertion author="Kenneth Kurtz"
date="2026-01-03T20:27:00Z"}training phase followed by a test phase [(no
feedback) including generalization items]{.insertion
author="Kenneth Kurtz" date="2026-01-03T20:27:00Z"}. The categories [to
be learned in the task]{.deletion author="Kenneth Kurtz"
date="2026-01-03T20:27:00Z"} were constructed so that [they]{.deletion
author="Kenneth Kurtz" date="2026-01-03T20:28:00Z"} both exhibited the
underlying regularity of a strong positive feature correlation[: two
parallel diagonal lines in 2D space, one for each category (Alpha versus
Beta).]{.insertion author="Kenneth Kurtz"
date="2026-01-03T20:29:00Z"}[.]{.deletion author="Kenneth Kurtz"
date="2026-01-03T20:29:00Z"} [feels like we should specify exactly what
is the same/different and why this is notable]{.comment-start id="80"
author="Kenneth Kurtz" date="2026-01-03T20:32:00Z"}This category
structure is notable for its likeness to Information-Integration (Ashby
& Maddox, 1990) and Condensation categories (Gottwald & Garner, 1972;
Kruschke, 1993). []{.comment-end id="80"}Figure 1 shows Alpha training
stimuli, Beta training stimuli, and test stimuli plotted in feature
space. Note that there are two distinct sets of test stimuli: one set of
test items (denoted by the letter Y) that falls on the Beta category
correlation line, and the other set of test items (denoted by the letter
X) that falls on the Alpha category correlation line. It is also
[critical]{.insertion author="Kenneth Kurtz"
date="2026-01-03T20:33:00Z"}[important]{.deletion author="Kenneth Kurtz"
date="2026-01-03T20:33:00Z"} to note that both groups of test items are
[need city-block specification and nosofsky citation]{.comment-start
id="83" author="Kenneth Kurtz"
date="2026-01-03T20:34:00Z"}equidistant[]{.comment-end id="83"} to
either of the contrasting sets of training items (see Figure 1).
Therefore, under the assumptions of the GCM, either category should be
equally likely to be generalized to [any]{.insertion
author="Kenneth Kurtz" date="2026-01-03T20:36:00Z"} [either of the
groups]{.deletion author="Kenneth Kurtz" date="2026-01-03T20:36:00Z"}
[of]{.deletion author="Kenneth Kurtz" date="2026-01-03T20:36:00Z"} test
item[s]{.deletion author="Kenneth Kurtz" date="2026-01-03T20:36:00Z"}
[in either group]{.insertion author="Kenneth Kurtz"
date="2026-01-03T20:36:00Z"}. However, under the coherence framework
offered by the DIVA model, subjects would be expected to incorporate the
way features cohere within a category in their knowledge
representations, leading to the leveraging of within-category feature
regularities upon generalization[, i.e., seeing X items as Alpha members
and Y items as Beta members]{.insertion author="Kenneth Kurtz"
date="2026-01-03T20:37:00Z"}. Such clearly divergent predictions from
the models of interest make this structure particularly well suited for
both computational and behavioral experiments. Predictions for both
models were confirmed by running simulations with a thorough sampling of
parameter space.

![](media/image1.png){width="3.84375in" height="3.8333333333333335in"}

[need a figure caption, be sure to clarify that A and B are used as
shorthand for Alpha and Beta labels.  it would be great to put this
graphic on a grid to make the distance relationships fully
clear!]{.comment-start id="90" author="Kenneth Kurtz"
date="2026-01-03T20:39:00Z"}**Figure 1**[]{.comment-end id="90"}

### Materials

[should we make a simple figure for this?]{.comment-start id="92"
author="Kenneth Kurtz"
date="2026-01-03T20:44:00Z"}Stimuli[]{.comment-end id="92"} were squares
varying in shading and size. The separability of these features
justifies using a city-block metric (Garner, 1974) for the determination
of psychological distance. Additionally, an independent scaling study
verified that the dimensions are nearly equal in perceptual salience.
Exemplars were automatically generated at 9 positions on each dimension
(9 shading \* 9 size = 81 examples).

### Procedure

Participants completed 96 training trials (12 blocks consisting of
[random-order presentation of the]{.insertion author="Kenneth Kurtz"
date="2026-01-03T20:45:00Z"}[the]{.deletion author="Kenneth Kurtz"
date="2026-01-03T20:45:00Z"} 8 training examples). On each trial, a
stimulus was presented on a computer screen and learners were prompted
to make a classification decision by clicking one of two buttons
(labeled 'Alpha' and 'Beta'). After selecting a class label, learners
were given feedback on their response. Following the training phase,
participants completed [need justification for sampling the whole grid
at test  we should probably refer to X and Y as \"critical\"
generalization items.  do we have data for the rest of the test grid? 
 i feel like reviewers will ask about this, so we need to figure out how
to talk about this.]{.comment-start id="96" author="Kenneth Kurtz"
date="2026-01-03T20:51:00Z"}81[]{.comment-end id="96"} generalization
trials consisting of items sampled at 9 positions on each dimension. All
of the training examples were included (intermixed). Feedback was not
provided during the generalization phase. Participants were informed
that there would be test trials prior to beginning the experiment.

## Results

### A Priori Simulation Results

Prior to collecting behavioral data, a computational experiment was run
to ensure that the present category structure was indeed a useful probe
into the question of whether subjects represent category knowledge based
solely on proximity to familiar exemplars (such as the GCM describes) or
based on richer knowledge about what makes a category coherent (such as
is suggested by the DIVA model). Both DIVA and GCM were trained and
tested on the present category structure. Model parameters were varied
[do we have the ranges, etc?]{.comment-start id="99"
author="Kenneth Kurtz"
date="2026-01-03T21:06:00Z"}thoroughly[]{.comment-end id="99"} to ensure
that the model's full behavioral repertoire was captured in the
simulations.

[redundant?]{.comment-start id="100" author="Kenneth Kurtz"
date="2026-01-03T21:07:00Z"}The training items exhibit a perfect within
category feature correlation and can be viewed as being separated by a
diagonal boundary that runs through the midpoint of the two lines of
correlation on which the two categories lie (see Figure
1).[]{.comment-end id="100"} [Our]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:07:00Z"} DIVA simulations revealed that the model
typically extends this diagonal boundary to the test items[:]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:07:00Z"} [--]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:07:00Z"} exemplars on the
Alpha category side of the extended boundary are more likely to be
classified as members of the Alpha category than exemplars on the other
side, and vice-versa (i.e., A → X, B → Y). [As shown in Figure 2, DIVA
can predict anywhere from a slight to strong global coherence basis for
categorizing the critical generalization items (depending on
parameterization).]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:10:00Z"} DIVA's performance [follows]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:14:00Z"}[is]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:14:00Z"}
[directly]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:14:00Z"}[concisely]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:14:00Z"} [from]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:14:00Z"}[explained by]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:14:00Z"} [[]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:14:00Z"}]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:14:00Z"} []{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:14:00Z"}its design
principles: because DIVA is trained on feature prediction (rather than
class prediction), the model learns that the features can be used to
predict one another. After training, DIVA reconstructs novel items
following its knowledge of each category's feature correlations,
affording an extension of the diagonal boundary.

In [our]{.deletion author="Kenneth Kurtz" date="2026-01-03T21:08:00Z"}
simulations with the exemplar model, we found that the GCM could not
[make the same predictive pattern shown by]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:08:00Z"}[mimic]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:08:00Z"} DIVA['s
performance]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:08:00Z"}. Instead of extending the diagonal boundary
[outward]{.deletion author="Kenneth Kurtz" date="2026-01-03T21:18:00Z"},
the GCM classifies each critical [generalization]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:18:00Z"} item with equal
probability [(see Figure 2)]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:18:00Z"}. [The GCM must behave this way
because]{.insertion author="Kenneth Kurtz" date="2026-01-03T21:19:00Z"}
[A close examination of the Diagonal classification explains the GCM's
performance:]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:19:00Z"} each of the critical items is equally
distant (under a city-block metric) to known members of both categories.
While a Euclidean metric would enable the GCM to extend each category to
its critical items, the use of a city-block metric reflects the
separable stimulus dimensions used in the behavioral experiment reported
below (see Garner, 1974). Cityblock distance was also supported by the
results of an independent scaling study with our materials[:]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:20:00Z"} [--]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:20:00Z"} critical items [in
groups]{.insertion author="Kenneth Kurtz" date="2026-01-03T21:20:00Z"} X
[and]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:20:00Z"}[&]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:20:00Z"} Y are not viewed as more similar to items
on their own side of the diagonal boundary. Thus, with evenly
distributed selective attention, the GCM classifies each item with a
probability of 0.5. Unequal allocation of the attention results in
uniform changes to the classification gradient -- for example, greater
allocation to the vertical (Y-axis) dimension results in increased
Category B probability for the entire collection of items in the
critical area. [These a priori results provide a compelling framework to
evaluate the behavioral results: the GCM predicts X and Y items to be
undifferentiated relative to the learned categories while DIVA predicts
a clear alignment of X to Alpha and Y to Beta.]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:25:00Z"}

Importantly, other types of reference points (i.e., prototypes,
clusters) also lead to the same performance[:]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:21:00Z"} [--]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:21:00Z"} the critical items
[area]{.deletion author="Kenneth Kurtz" date="2026-01-03T21:21:00Z"} are
also equally close to the category prototypes [of Alpha and
Beta]{.insertion author="Kenneth Kurtz" date="2026-01-03T21:21:00Z"}, as
well as a variety of [potential]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:21:00Z"} cluster configurations. The GCM's results
therefore characterize a set of predictions made by ['similarity to
stored]{.insertion author="Kenneth Kurtz" date="2026-01-03T21:22:00Z"}
reference point[s']{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:22:00Z"} [accounts]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:22:00Z"}[models]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:22:00Z"} more generally.

![](media/image2.png){width="4.78125in" height="4.65625in"}

[how about we take the behavioral result out of Fig 2 and also add a new
figure (this one) that includes the behavioral result after those data
are reported?]{.comment-start id="139" author="Kenneth Kurtz"
date="2026-01-03T21:24:00Z"}**Figure 2:** *A priori* simulations
w[]{.comment-end id="139"}ith DIVA and the GCM. Densities in this plot
reflect predictions about the classification of critical items, across
many different parameter settings. Positive scores indicate that each
category was generalized to the items on its side of the diagonal
boundary that lies between the two sets of training items, *A → X*, *B →
Y*.

### Behavioral Results

By the end of the training phase, most participants had successfully
mastered the categories. On average, participants were 89.2% (SE = 2.5)
accurate during the last training block. Only two of 30 participants
failed to reach greater than 6/8 correct during the final training
block. Aggregate training data is depicted in the left panel of Figure
3. As a test of whether learners extended the diagonal boundary, we
compared the average number of Alpha classification responses made to
critical items [in groups]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:30:00Z"} X [and]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:30:00Z"}[&]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:30:00Z"} Y (Figure 3, right panel). Learners
systematically generalized each category -- participants were more
likely to produce an Alpha response to X than to Y,[formatting, italics,
etc]{.comment-start id="144" author="Kenneth Kurtz"
date="2026-01-03T21:31:00Z"} t(29) = 5.02, p \< 0.001, d = 0.56.
[]{.comment-end id="144"}We then compared the difference score we
obtained behaviorally (X −Y) to our a priori results with DIVA and the
GCM: as shown in [maybe we\'ll call the second one Figure
2b?]{.comment-start id="145" author="Kenneth Kurtz"
date="2026-01-03T21:32:00Z"}Figure 2,[]{.comment-end id="145"} the
difference score we observed cannot be explained by the GCM, but [falls
quite centrally in the range of predictions made by the]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:32:00Z"} [is fully explained
by the]{.deletion author="Kenneth Kurtz" date="2026-01-03T21:32:00Z"}
DIVA model. Aggregate generalization data is depicted in Figure 4.

![](media/image3.png){width="6.5in" height="2.9027777777777777in"}

**Figure 3**

### Post-hoc Simulation Results

The overall goal of the following simulations is to formally evaluate
the performance of DIVA and the GCM in terms of quantitative fit to
[the]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:34:00Z"}[our]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:34:00Z"} observed generalization behavior. Before
proceeding, it is worth noting that DIVA and the GCM are not fully
comparable: unlike the GCM, DIVA's category representations are
constrained via back-propagation learning (Rumelhart et al., 1986), and
its performance is stochastic. However, model performance on
generalization testing can still be compared to assess whether [the
present]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:34:00Z"}[our]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:34:00Z"} results can be explained under a reference
point [approach]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:34:00Z"}[scheme]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:34:00Z"}.

We used parameter optimization techniques to find each model's best fit
to the observed generalization data using a mean-squared error (MSE)
metric. We used a hill climbing procedure to fit the GCM over four
parameters: exemplar specificity (c), response mapping (γ), and
attention strengths for features 1 and 2 (W1 and W2). DIVA's behavior is
stochastic, which precludes the use of hill-climbing. Consequently, we
searched for DIVA's best fit using a 'grid-search' technique to generate
predictions along a range of settings for its four parameters: number of
hidden units, learning rate, initial weight range, and a focusing
parameter, β (Kurtz, 2015). [do we need to give these kind of details
for the a priori simulations?]{.comment-start id="155"
author="Kenneth Kurtz" date="2026-01-03T21:35:00Z"}At each point, DIVA
was initialized 2000 times with random small-valued weights and a random
presentation sequence. The model used logistic hidden units and linear
outputs. Attention weighting was allowed to vary freely in both models
even though both dimensions are equally relevant toward solving the
classification.[]{.comment-end id="155"}

Overall, DIVA was able to provide a stronger fit to the full behavioral
gradient than the GCM. DIVA's best fit (MSE = 0.006) was achieved with 3
hidden units, learning rate = 0.55, weight range ±0.5, and β = 3. The
GCM's best fit (MSE = 0.0075) was achieved with c = 5.304, γ = 1.055, W1
= 0.507, W2 = 0.493. Model performance further differentiated the
responses to the critical items (rather than the entire gradient): DIVA
achieved MSE = 0.0037, and the GCM achieved MSE = 0.02. [This wider gap
reflects both models providing a good overall fit, but GCM failing in
the critical generalization region.]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:37:00Z"} Beyond quantitative fitting[,
however]{.deletion author="Kenneth Kurtz" date="2026-01-03T21:39:00Z"},
it is important to [note]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:39:00Z"}[acknowledge]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:39:00Z"} that DIVA's
predictions match the qualitative patterns of observed performance --
the model extends each category to novel items along the diagonal
boundary. Conversely, the GCM's generalization is completely neutral for
these items. Each model's best performance is depicted in Figure 4.

![](media/image4.png){width="6.5in" height="2.3472222222222223in"}

[caption needed]{.comment-start id="160" author="Kenneth Kurtz"
date="2026-01-03T21:40:00Z"}**Figure 4**[]{.comment-end id="160"}

## Discussion

Experiment 1 provides [strong]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:41:00Z"}[clear]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:41:00Z"} evidence that human category learning can
be based on extracted feature regularities rather than similarity to
stored exemplars. When presented with novel items equidistant from both
categories\' training examples, subjects systematically generalized
based on learned feature correlations. Items that fell along a
category\'s correlation line were classified as belonging to that
category, despite being no more similar to its exemplars than to the
contrast category\'s exemplars.

This pattern is precisely what DIVA predicts based on its architecture
for learning within-category feature relationships, but it cannot be
explained by the GCM regardless of parameter settings. The computational
simulations confirmed that exemplar-based models predict chance-level
responding to these critical items, while DIVA predicts the
[systematic]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:47:00Z"} extension of correlation-based boundaries
[as]{.insertion author="Kenneth Kurtz" date="2026-01-03T21:47:00Z"}[that
we]{.deletion author="Kenneth Kurtz" date="2026-01-03T21:47:00Z"}
[]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:47:00Z"}observed behaviorally.

Th[is compelling effect]{.insertion author="Kenneth Kurtz"
date="2026-01-03T21:47:00Z"} [e strength of this effect---subjects
showed consistent generalization patterns that provided superior
quantitative fit to DIVA (MSE = 0.006) compared to GCM (MSE =
0.0075)---]{.deletion author="Kenneth Kurtz"
date="2026-01-03T21:47:00Z"}suggests that coherence-based
representations can dominate similarity-based processing when category
structure supports it. Both categories in this experiment exhibited
perfect feature correlations, making correlation-based representation
viable for the entire domain.

This finding demonstrates that when categories possess clear internal
structure, human learners extract and utilize this structure for
generalization in ways that go beyond exemplar similarity. The next
experiments examine how this process is influenced by domain
characteristics and the strength of correlational structure.

# [goals, transition from E1, introduce learning mode component with rationale and predictions, why drop modeling,]{.comment-start id="171" author="Kenneth Kurtz" date="2026-01-03T22:42:00Z"}[E2-specific intro]{.comment-start id="172" author="Kenneth Kurtz" date="2026-01-03T21:48:00Z"}Experiment 2[[]{.comment-end id="171"}]{.comment-end id="172"}

## Methods

### Participants

[sample size]{.comment-start id="175" author="Kenneth Kurtz"
date="2026-01-03T21:50:00Z"}Ninety-six[]{.comment-end id="175"}
undergraduate students participated to receive partial fulfillment of a
course requirement.

### Design

This experiment tested whether coherence-based representations emerge
when only one category in a domain has strong internal structure. The
Alpha category exhibited perfect positive feature correlation while the
Beta category had weak, inconsistent structure (see Figure 5). Critical
test items (T3, T4) lay along the Alpha correlation line but were more
similar to Beta exemplars[; thereby]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:23:00Z"}[,]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:23:00Z"} creating a direct conflict between
coherence-based and similarity-based generalization.

We [explain why?]{.comment-start id="179" author="Kenneth Kurtz"
date="2026-01-03T22:24:00Z"}also[]{.comment-end id="179"} manipulated
learning mode to test whether task demands influence representational
strategy. [we should also explain the specific choices of the additional
categories and why we bother to collect the training phase II
data\...]{.comment-start id="180" author="Kenneth Kurtz"
date="2026-01-03T22:34:00Z"}[since this is a novel manifestation of a
generative mode, we should say some more about it, justify its use, and
compare it to previous work (inference, observational)]{.comment-start
id="181" author="Kenneth Kurtz" date="2026-01-03T21:53:00Z"}The
generative condition informed subjects they would later learn additional
categories (Figure 6), potentially encouraging richer within-category
knowledge[[]{.comment-end id="180"}]{.comment-end id="181"}. The
discriminative condition used standard two-[way]{.insertion
author="Kenneth Kurtz" date="2026-01-03T21:53:00Z"}[category]{.deletion
author="Kenneth Kurtz" date="2026-01-03T21:53:00Z"} classification.

If subjects extract correlational structure when[ever]{.insertion
author="Kenneth Kurtz" date="2026-01-03T22:24:00Z"} available, [do we
need to mark T3 and T4 in Fig 5?]{.comment-start id="185"
author="Kenneth Kurtz" date="2026-01-03T21:54:00Z"}T3 and T4
[]{.comment-end id="185"}should be classified as Alphas despite their
proximity to Beta items. If [learners]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:25:00Z"}[subjects]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:25:00Z"} rely primarily on exemplar similarity,
these items should be classified as Betas.

![](media/image5.png){width="6.5in" height="4.875in"}**F[i]{.insertion
author="Kenneth Kurtz" date="2026-01-03T20:23:00Z"}[I]{.deletion
author="Kenneth Kurtz" date="2026-01-03T20:23:00Z"}gure 5***:
Illustration of category structure used during training phase 1 and test
phase. Blue Betas represent training items for the Beta category. Red
Alphas [R]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:28:00Z"}[r]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:28:00Z"}epresent training items for the Alpha
category. Yellow T's represent novel items introduced during the test
phase. All stimuli were monochromatic squares that varied along two
dimensions[:]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:28:00Z"}[-]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:28:00Z"}* [[]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:28:00Z"}]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:28:00Z"} *size and shading.*

![](media/image6.png){width="6.5in" height="4.875in"}***Figure 6**:
Illustration of the category structure used during training phase 2.
Blue Betas represent training items for the Beta category. Red Alphas
[R]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:30:00Z"}[r]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:30:00Z"}epresent training items for the Alpha
category. Black Gammas represent training items for the Gamma Category.
Green Deltas [R]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:30:00Z"}[r]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:30:00Z"}epresent training items for the Delta
Category. All stimuli were monochromatic squares that varied along two
dimensions[:]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:30:00Z"}[-]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:30:00Z"} size and shading.*

### Materials

Stimuli consisted of monochromatic squares that varied along two
dimensions: size and gray-scale shading. Figures [5]{.insertion
author="Kenneth Kurtz" date="2026-01-03T22:34:00Z"}[1]{.deletion
author="Kenneth Kurtz" date="2026-01-03T22:34:00Z"} and [6]{.insertion
author="Kenneth Kurtz" date="2026-01-03T22:34:00Z"}[2]{.deletion
author="Kenneth Kurtz" date="2026-01-03T22:34:00Z"} show the stimuli
plotted with size on the y-axis and shading on the x-axis. A shading
value of 0.0 translates to a completely black square, while a shading
value of 1.0 translates to a completely white square.

### Procedure

Subjects in the Generative condition were told that they would be tasked
with learning four categories of geometric shapes (Alphas, Betas,
Gammas, and Deltas), but that they would first focus on learning about
Alphas and Betas and that Gammas and Deltas would come later. During
each training trial, a stimulus [would]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:35:00Z"} appear[ed]{.insertion
author="Kenneth Kurtz" date="2026-01-03T22:35:00Z"} [at]{.insertion
author="Kenneth Kurtz" date="2026-01-03T22:35:00Z"}[on]{.deletion
author="Kenneth Kurtz" date="2026-01-03T22:35:00Z"} the center of the
screen along with text asking [to]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:35:00Z"} which category the stimulus
belong[s]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:35:00Z"}[ed]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:35:00Z"} [to]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:35:00Z"}. At the bottom of the screen there was a
row of four buttons with labels corresponding to each of the four
categories; however, the Gamma and Delta buttons were gray-ed out and
nonfunctional. After submitting a response via mouse-click, subjects
received [corrective]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:36:00Z"} feedback. Training was split into blocks in
which each of the 12 training stimuli (6 per category) would appear once
in random order. If a subject completed a block with an accuracy of 11
out of 12 correct responses, they were allowed to move on to the next
phase of the experiment[;]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:36:00Z"}[-]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:36:00Z"} subjects were allowed a maximum of 8 blocks
to reach this criterion.

The next phase of the experiment was the test phase which was delivered
in the same way as the training phase except that no feedback was
given[,]{.deletion author="Kenneth Kurtz" date="2026-01-03T22:36:00Z"}
and novel test items were included. Each of the previously learned items
along with five novel test items were presented once in random order
(i.e., the test phase consisted of 17 trials with order randomized
[across subjects]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:37:00Z"}).

The final phase of the experiment was the second training phase in which
Gamma and Delta items were included among the original Alpha and Beta
training items (none of the previously novel items from the test phase
were included in the second training phase). The second training phase
consisted of two blocks in which each item was presented once in random
order.

The procedure for the Discriminative condition was identical to that of
the Generative condition except that Discriminative condition subjects
were not made aware of the Alpha and Gamma categories (neither via
instructions nor presence of response buttons) until the second training
phase.

### [let\'s talk about this in the E2 intro so it doesn\'t come as a surprise.  there is a compelling counter-argument that we could simply model the discriminative conditions, so we ought to either do that or explain why we don\'t.  we could try to say this isn\'t a model comparison experiment \-- that we are primarily interested in behavioral questions after E1.  we\'d have to make this case clearly and effectively or reviewers are going to balk\...  because it does seem like it would be interesting to know what DIVA does when the correlation only holds for one category.]{.comment-start id="223" author="Kenneth Kurtz" date="2026-01-03T22:50:00Z"}[Will do sims actually. Just ignoring the learning mode manipulation for the sims. A good model should be able to capture behavior regardless of learning mode of the subjects.]{.comment-start id="224" author="Joshua Glass" date="2026-11-12T13:53:00Z"}Model Simulations

[Unlike Experiment 1, we did not conduct computational simulations for
this experiment. The learning mode manipulation (generative vs.
discriminative context) involves high-level strategic and metacognitive
factors that are not straightforward to implement in current
computational models like DIVA or GCM. These models operate at the level
of feature processing and similarity computation, but do not incorporate
mechanisms for subjects\' beliefs about future task demands or strategic
choices about representational approaches.[]{.comment-end
id="223"}]{.deletion author="Joshua Glass"
date="2026-11-12T13:52:00Z"}[]{.comment-end
id="224"}[]{.paragraph-deletion author="Joshua Glass"
date="2026-11-12T13:52:00Z"}

[Additionally, the core predictions about coherence-based versus
similarity-based generalization follow the same principles as Experiment
1, where we established clear divergent predictions through systematic
simulation. The Alpha category in the current experiment exhibits the
same perfect positive correlation as both categories in Experiment 1,
while critical test items create the same conflict between correlational
structure and exemplar similarity. [i\'m not sure about this!  the
shared hidden layer across channels calls this into question, doesn\'t
it?]{.comment-start id="230" author="Kenneth Kurtz"
date="2026-01-03T22:52:00Z"}We can therefore be confident that DIVA
would predict coherence-based generalization []{.comment-end
id="230"}(Alpha responses to T3 and T4) while GCM would predict
similarity-based generalization (Beta responses to T3 and
T4).]{.deletion author="Joshua Glass"
date="2026-11-12T13:52:00Z"}[]{.paragraph-deletion author="Joshua Glass"
date="2026-11-12T13:52:00Z"}

## Results

### Training Phase 1 Performance

Twenty-seven subjects failed to meet the predetermined learning
criterion (11 out of 12 correct responses within a block) and were
excluded from analysis. The remaining subjects (Discriminative: n = 35,
Generative: n = 34) showed nearly identical learning curves across
conditions, with most reaching criterion well before the maximum of 8
blocks (Figure 7). When constructing learning curves in these cases, it
was assumed (as has been assumed by others; see Nosofsky et al., 1994)
that performance would be maintained at criterion if the subject
remained sufficiently engaged[; therefore]{.insertion
author="Kenneth Kurtz" date="2026-01-03T22:53:00Z"}[-]{.deletion
author="Kenneth Kurtz" date="2026-01-03T22:53:00Z"} []{.insertion
author="Kenneth Kurtz" date="2026-01-03T22:53:00Z"}when subjects were
missing block [scores]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:53:00Z"}[accuracies]{.deletion
author="Kenneth Kurtz" date="2026-01-03T22:53:00Z"} due to reaching
criterion early, criterion accuracy was used to fill []{.insertion
author="Kenneth Kurtz" date="2026-01-03T22:53:00Z"}[-]{.deletion
author="Kenneth Kurtz" date="2026-01-03T22:53:00Z"}in the missing data
(Figure 4).

![](media/image7.png){width="6.5in" height="4.875in"}*Figure 7: Learning
curves for Generative and Discriminative conditions* *[in Experiment
2]{.insertion author="Kenneth Kurtz"
date="2026-01-03T22:54:00Z"}[.]{.deletion author="Kenneth Kurtz"
date="2026-01-03T22:54:00Z"}*

### Test Phase Performance

We examined generalization to critical test items[reviewers will ask
about T1-5]{.comment-start id="243" author="Kenneth Kurtz"
date="2026-01-03T22:56:00Z"} T3 and T4,[]{.comment-end id="243"} which
lie along the Alpha category\'s correlation line but are more similar to
Beta exemplars. If subjects developed coherence-based representations of
the Alpha category, these items [let\'s talk about how this is a more
demanding test than E1 because now there is a clear exemplar similarity
choice rather than exemplar similarity neutrality.  that\'s important
right?  also, i\'d like to document this specifically (the exact
distances to near exemplars)]{.comment-start id="244"
author="Kenneth Kurtz" date="2026-01-03T22:59:00Z"}should be classified
a[]{.comment-end id="244"}s Alphas despite their proximity to Beta
training items.

The aggregate results showed that both critical items were predominantly
classified as Betas across both conditions (Figure 8), consistent with
similarity-based rather than coherence-based generalization. However,
individual differences analysis revealed that [small]{.deletion
author="Kenneth Kurtz" date="2026-01-03T23:00:00Z"} subsets of subjects
did show coherence-consistent patterns. [do we want to contextualize
this in terms of the 1/3 rate in the published partial XOR
paper?]{.comment-start id="246" author="Kenneth Kurtz"
date="2026-01-03T23:02:00Z"}[Good idea. Definitely do
this.]{.comment-start id="247" author="Joshua Glass"
date="2026-11-12T13:52:00Z"}Nine subjects (26%) [[]{.comment-end
id="247"}]{.comment-end id="246"}in the Discriminative condition
classified T3 and/or T4 as Alphas[, [i don\'t think it is good form to
talk about this one data point, ok to drop it?]{.comment-start id="249"
author="Kenneth Kurtz" date="2026-01-03T23:01:00Z"}with one subject
showing the clearest coherence-based pattern: both T3 and T4 classified
as Alpha[]{.comment-end id="249"}, T5 as Beta, and high accuracy on
training items]{.deletion author="Joshua Glass"
date="2026-11-12T13:49:00Z"}. Six subjects (18%) in the Generative
condition showed similar patterns[.]{.insertion author="Joshua Glass"
date="2026-11-12T13:50:00Z"}[, [ok to drop?]{.comment-start id="252"
author="Kenneth Kurtz" date="2026-01-03T23:01:00Z"}though none as
clearly as the best Discriminative condition generalizer.]{.deletion
author="Joshua Glass" date="2026-11-12T13:50:00Z"}[]{.comment-end
id="252"}

Notably, the Generative condition [can\'t say this without getting into
significance testing, right?]{.comment-start id="253"
author="Kenneth Kurtz" date="2026-01-03T23:03:00Z"}[Yes. Need to do some
proportion testing.]{.comment-start id="254" author="Joshua Glass"
date="2026-11-12T13:51:00Z"}showed a lower proportion [[]{.comment-end
id="254"}]{.comment-end id="253"}of coherence-based generalization than
the Discriminative condition, [contrary to our[i\'m not sure we made a
clear prediction!]{.comment-start id="256" author="Kenneth Kurtz"
date="2026-01-03T23:03:00Z"}[Good point need to reframe.]{.comment-start
id="257" author="Joshua Glass" date="2026-11-12T13:50:00Z"} initial
prediction]{.deletion author="Joshua Glass"
date="2026-11-12T13:50:00Z"}[[]{.comment-end id="257"}]{.comment-end
id="256"} [but]{.deletion author="Joshua Glass"
date="2026-11-12T13:50:00Z"} consistent with a [need to clarify what is
meant by this]{.comment-start id="259" author="Kenneth Kurtz"
date="2026-01-03T23:04:00Z"}domain-general strategy
interpretation[]{.comment-end id="259"} (see Discussion).

![](media/image8.png){width="6.5in"
height="2.7222222222222223in"}*Figure 8: Average generalization profiles
for Generative and Discriminative conditions. Stimuli are plotted as
points in feature space. Outer circles indicate the experimenter defined
identities of the stimuli, while inner circles represent average subject
response. The inner circles vary along a blue-red color gradient: the
blue and red end of the gradients represent high proportions of Beta and
Alpha responding respectively.*

![](media/image9.png){width="6.5in" height="4.875in"}*Figure 9:*[i think
we can make some more nuanced comments about these graphs.  the blue
item closest to the reds is often gotten wrong.  T1 and T2 are often
accepted as reds despite being somewhat off the diagonal.  T3 is a
better bet to be correlational generalized because it is nearer to the
training group than T4.  and T4 is also much nearer to a blue training
item. the generative subgroup has idiosyncratic stuff:  neutral
performance on 4 training items]{.comment-start id="260"
author="Kenneth Kurtz" date="2026-01-03T23:12:00Z"} *Average
generalization response from 9 Discriminative condition subjects who
classified T3 and/or T4 as Alpha(s).*[]{.comment-end id="260"}

![](media/image10.png){width="6.5in" height="4.875in"}*Figure 10:
Average generalization response from 6 Generative condition subjects who
classified T3 and/or T4 as Alpha(s).*

### [or we could just add a footnote:  we collected phase 2 learning data with additional categories but found nothing of clear interest]{.comment-start id="262" author="Kenneth Kurtz" date="2026-01-04T01:18:00Z"}[training phase 2 isn\'t looking like something you\'d see in a good journal.  what happens if we drop it?]{.comment-start id="263" author="Kenneth Kurtz" date="2026-01-04T01:11:00Z"}Training Phase 2 Performance

Introduction of Gamma and Delta categories in the second training phase
showed equivalent performance across conditions (both \~50% accuracy,
above chance for 4-category classification; Figure 11).[[]{.comment-end
id="262"}]{.comment-end id="263"}

![](media/image11.png){width="6.5in" height="4.875in"}Figure 11:
Training Phase 2 learning curves for both Generative and Discriminative
conditions.

### [Exploratory Analysis]{.deletion author="Joshua Glass" date="2026-11-12T13:48:00Z"}

[need some introduction to this about what was the point of this , why
is it exploratory, etc]{.comment-start id="268" author="Kenneth Kurtz"
date="2026-01-04T01:19:00Z"}[I don't think this is really worth
reproting and discussing. More of a distraction.]{.comment-start
id="269" author="Joshua Glass" date="2026-11-12T13:47:00Z"}[An
exploratory analysis revealed systematic reclassification of specific
training items during test. [[]{.comment-end id="269"}]{.comment-end
id="268"}Items [need to mark these in the figure, yes?]{.comment-start
id="271" author="Kenneth Kurtz" date="2026-01-04T01:52:00Z"}A6 (Alpha
category) and B4 (Beta category) []{.comment-end id="271"}showed
significantly lower test accuracy compared to other training items in
both conditions \[Discriminative: Alpha items F(29,5) = 5.83, p \< .001;
Beta items F(29,5) = 15.10, p \< .001; Generative: Alpha items F(28,5) =
5.52, p \< .001; Beta items F(28,5) = 10.71, p \< .001\].]{.deletion
author="Joshua Glass" date="2026-11-12T13:48:00Z"}[]{.paragraph-deletion
author="Joshua Glass" date="2026-11-12T13:48:00Z"}

[cite nosofsky on learning during testing?]{.comment-start id="274"
author="Kenneth Kurtz" date="2026-01-04T01:24:00Z"}[Importantly, this
reclassification was not simply due to poor initial learning. Fisher\'s
Exact Tests comparing final training block accuracy to test accuracy
showed significant decreases for item B4 in both conditions
(Discriminative: p = .004; Generative: p = .004) and for item A6 in the
Generative condition (p = .03), indicating that subjects systematically
changed their classification of these previously mastered items during
the no-feedback test phase.[]{.comment-end id="274"}]{.deletion
author="Joshua Glass" date="2026-11-12T13:48:00Z"}[]{.paragraph-deletion
author="Joshua Glass" date="2026-11-12T13:48:00Z"}

## [i\'m thinking maybe we shift the framing for this exp a little \-- we find this surprising effect in E1 and now we say: what are some interesting ways to push on it \-- namely, can we make it stronger with a more generative learning mode (we invent a new way to encourage gen mode that does not change the core classification task) and does the coherence phenomenon hold up under less than the ideal circumstances of perfect full domain coherence and critical test items that are completely neutral by exemplar similarity.  we conclude that we still see traces of the coherence mechanism but the main story is clear limits on the phenomenon \-- and the generative mode showed no signs of overcoming these limits.]{.comment-start id="277" author="Kenneth Kurtz" date="2026-01-04T02:10:00Z"}Discussion[]{.comment-end id="277"}

Experiment 2 yielded mixed evidence for coherence-based representation.
The majority of subjects classified critical items based on
[exemplar]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:25:00Z"} similarity rather than correlational
structure, with only [small]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:24:00Z"} subsets (9/35 discriminative, 6/34
generative) showing coherence-consistent patterns. This contrasts
sharply with Experiment 1[,]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:24:00Z"} where coherence-based generalization was
the dominant pattern.

The key difference appears to be domain structure. Experiment 1 used two
categories that both exhibited perfect correlations, making
correlation-based representation viable domain-wide. Experiment 2
included one structured and one unstructured category[;]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:25:00Z"}[,]{.deletion
author="Kenneth Kurtz" date="2026-01-04T01:25:00Z"} [making
similarity-based representation more generally applicable across the
domain. W]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:26:00Z"}[w]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:26:00Z"}hen coherence-based strategies work for some
categories but not others, subjects may default to [an]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:27:00Z"} [the more
domain-general]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:27:00Z"} [exemplar]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:27:00Z"}
similarity[-based]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:27:00Z"} approach. [It could also be that a
constraint on the learning of featural regularities is the need to
pertain to both categories. This result does nothing to undermine the
important phenomenon captured in Experiment 1, but it suggests that,
just as there are limits on what reference point similarity can account
for, there are also limits on the ability to learn by inducing a
statistical model of featural regularities. A potential interpretation
is that the property of global coherence needs to hold at the domain
level (all categories contributing to the coherence) in order for it to
guide category formation and generalization. That said, it is still
notable that a non-trivial subset of learners showed a tendency toward
extending the diagonal of the coherent category.]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:27:00Z"}

[Importantly, t]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:40:00Z"}[T]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:40:00Z"}he learning [mode]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:40:00Z"}[context]{.deletion
author="Kenneth Kurtz" date="2026-01-04T01:40:00Z"} manipulation [not
only]{.deletion author="Kenneth Kurtz" date="2026-01-04T01:40:00Z"}
failed to increase coherence-based learning in the generative
conditio[n.]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:40:00Z"} [n---it actually reduced it.]{.deletion
author="Kenneth Kurtz" date="2026-01-04T01:40:00Z"} [There are several
possible explanations. First, the novel approach to inviting a
generative approach might have failed. Secondly, it could be the case
that encouraging a generative approach is not a valid way to promote
coherence-based concept acquisition. Third, it could be a matter of
[]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:40:00Z"}]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:40:00Z"}[This counterintuitive finding becomes
theoretically sensible when considered from the perspective
of]{.deletion author="Kenneth Kurtz" date="2026-01-04T01:40:00Z"}
strategic adaptation to domain demands[:]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:45:00Z"}[.]{.deletion
author="Kenneth Kurtz" date="2026-01-04T01:45:00Z"} [S]{.deletion
author="Kenneth Kurtz" date="2026-01-04T01:45:00Z"}[s]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:45:00Z"}ubjects in the
generative condition were explicitly told they would later need to learn
additional categories within the same domain[. T]{.deletion
author="Kenneth Kurtz" date="2026-01-04T01:45:00Z"}[, and t]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:45:00Z"}his [could
have]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:45:00Z"}[should]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:45:00Z"} motivate[d]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:45:00Z"} them to adopt
representational strategies [likely]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:45:00Z"}[that]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:45:00Z"} [to]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:45:00Z"}[will]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:45:00Z"} prove broadly useful across multiple
categories rather than strategies optimized for individual categories.

[overkill?]{.comment-start id="313" author="Kenneth Kurtz"
date="2026-01-04T01:46:00Z"}In the current domain, similarity-based
representation works for both the structured Alpha category and the
unstructured Beta category, making it the superior domain-general
strategy. Coherence-based representation, while potentially useful for
Alpha items, offers no advantage for Beta items and would require
subjects to maintain multiple representational systems. Generative
learners, anticipating the need to handle diverse category types, may
therefore be more likely to converge on the similarity-based approach
that will serve them well throughout the domain.[]{.comment-end
id="313"}

Th[e mixed results in this experiment and the outcome of the generative
learning mode]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:46:00Z"}[is interpretation]{.deletion
author="Kenneth Kurtz" date="2026-01-04T01:46:00Z"} [[]{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:46:00Z"}]{.deletion
author="Kenneth Kurtz" date="2026-01-04T01:46:00Z"} []{.insertion
author="Kenneth Kurtz" date="2026-01-04T01:46:00Z"}suggest[s]{.deletion
author="Kenneth Kurtz" date="2026-01-04T01:47:00Z"} that the adoption of
coherence-based versus similarity-based strategies is not simply a
matter of detecting correlational structure, but involves [sensitivity
to the task context including the set of categories being learned
together. [and the]{.deletion author="Kenneth Kurtz"
date="2026-01-04T01:48:00Z"}]{.insertion author="Kenneth Kurtz"
date="2026-01-04T01:48:00Z"} [a more sophisticated assessment of which
representational approach will prove most useful given the broader task
context]{.deletion author="Kenneth Kurtz" date="2026-01-04T01:48:00Z"}.
[let\'s tread lightly, i don\'t think we have the goods to make strong
claims about what\'s going on with the learning modes]{.comment-start
id="324" author="Kenneth Kurtz"
date="2026-01-04T01:57:00Z"}Discriminative learners, focused only on
distinguishing the current two categories, may be more willing to
exploit category-specific regularities even if they won\'t generalize
broadly. Generative learners, planning for future categories, may
prioritize representational consistency over local
optimization.[]{.comment-end id="324"}

[i think we need a stronger story here or its not worth getting into the
reclassification.  got anything?]{.comment-start id="326"
author="Kenneth Kurtz" date="2026-01-04T01:55:00Z"}[I think maybe this
is now worth discussing.]{.comment-start id="327" author="Joshua Glass"
date="2026-11-12T13:45:00Z"}[An unexpected finding was systematic
reclassification of previously learned items A6 and B4 during testing.
Despite being mastered during training, these items were frequently
misclassified at test. This occurred even without nearby test items that
could explain the shift through similarity-based processes, suggesting
that subjects\' category representations were not simply collections of
stored training examples but involved some form of structured knowledge
that could override item-specific learning.[[]{.comment-end
id="327"}]{.comment-end id="326"}]{.deletion author="Joshua Glass"
date="2026-11-12T13:45:00Z"}[]{.paragraph-deletion author="Joshua Glass"
date="2026-11-12T13:45:00Z"}

# [need intro that emphasizes narrative flow of why this exp makes sense after E1-2]{.comment-start id="330" author="Kenneth Kurtz" date="2026-01-04T02:10:00Z"}Experiment 3[]{.comment-end id="330"}

## Methods

### Participants

### Design

### Materials

Stimuli were of the same type as that used in experiment one and two
(i.e., squares that varied along the dimensions of size and shading).

### Procedure

### Model Simulations

## Results

### Training Phase Performance

### Test Phase Performance

## Discussion

# General Discussion

[Will import from mendeley]{.comment-start id="342"
author="Joshua Glass" date="2025-12-10T20:29:00Z"}REFS[]{.comment-end
id="342"}
