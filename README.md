![ScreenShot](https://github.com/peterwaksman/Narwhal/blob/master/NarwhalInPython.png)
Narwhal is a class library for Natural Language Processing in a "narrow world". It uses client defined key words and key narratives to initialize text aware classes, applying methods of geometry rather than statistics. These classes can read text from a narrow world and perform sentiment analysis or plain text-to-data-structure conversion. 

A <B>narrow world</B> is a collection of related topics with many short text examples and a underlying information model. For example TripAdvisor hotel reviews are a narrow world with roughly 30 common topics such as noise, wifi, service, nearby attractions, food, transportation, etc; and the information model is any data structure storing the hotel's attributes of interest. To read text from a narrow world, a client can focus on domain specific knowledge, while Narwhal does the text processing. For example, use Narhwal to build specialized chatbots rather than all purpose ones. Narwhal processes language through a "white box" of geometry rather than a "black box" of statistics and this, in particular, allows detailed analysis of short text fragments.


The concept of a narrow world is essentially the same as a “semantic frame” as described by Fillmore [Fillmore] and archived at Berkeley's "FrameNet"; however the process for extracting what has been said is implemented using the general method of “Best Model Classification” and “The Elements of Narrative” [WAKSMAN]. Narhwal is intended as a reference implementation and proof of the concept for the "moving topic". 

Other spellings (for the fussy GitHub search engine) trip advisor, trip-advisor, chat bot, chat-bot, nlp, frame net, keyword, keynarrative

