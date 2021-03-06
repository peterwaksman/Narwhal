﻿![ScreenShot](https://github.com/peterwaksman/Narwhal/blob/master/DOCS/CLogo.png)


 - See "QuickStart.txt" for tutorial sketch 
 - See "examples" and "narhwal_noise" for more complete examples of Narwhal applications.
 - See DOCS for Narwhal specification, hints for debugging, etc. 

 - See "nwchat.py" for chat template (under development)
 A now NEW AND IMPROVED - sample chatbots for:
     * a 'scene editor' using more-or-less structured commands 
     * an 'about chatbot' for greetings and answering questions
     * a 'confirm chatbot' for getting and confirming a string from the client.
     * a 'command chatbot' that expects structured language - with flexibility
     * an 'faq' chatbot that gets nowhere. It was in the midst of that, when I realized
something more was needed for conversational context.

Chatbot development is undergoing major changes as the nwcontext.py begins to
take shape. I moved all old chatbots to the 'examplesOldChatbots' folder. The dental 
vocabulary lives on in the mouthContext example.

Narwhal is a library of objects that can read text. It uses keywords based on client-provided synonym lists and also client-provided formulas in the keywords. So the client can focus on the details of the topic vocabularies and how people express themselves, rather than on how language works. While relying on Narwhal to understand the incoming language the client must still write code that transfers information from the Narwhal objects into more convenient data structures. 

The Narwhal approach is to embed detailed topic knowledge. This is called "narrow world language processing". Here, the "narrow world" of the client's topics is essentially the same thing as a semantic "frame” as described by Fillmore and archived at Berkeley's FrameNet.

Inquiries are welcome.