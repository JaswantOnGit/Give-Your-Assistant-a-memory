# Give-Your-Assistant-a-memory
<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Give Your Assistant a Memory

**Project Link:** [View Project](http://learn.nextwork.org/projects/ai-openclaw-memory)

**Author:** jaswant singh  
**Email:** jaswants022@gmail.com

---

---

## Introducing Today's Project!

In this project, I am transforming my OpenClaw Telegram assistant from a simple chatbot into a persistent, personalized AI assistant with memory.

I am setting up OpenClaw’s workspace memory system using two key files:

SOUL.md → defines my assistant’s personality, tone, and communication style
USER.md → teaches my assistant who I am (my preferences, background, and context)

As I interact with the assistant, it automatically creates and updates daily notes, allowing it to remember past conversations and carry context across sessions. This means my assistant doesn’t reset every time I get a more continuous and natural experience.

By the end of this project, my assistant:

Has a consistent personality and voice
Understands and remembers me over time
Maintains memory across conversations using stored notes
Functions more like an intelligent, evolving AI agent instead of a basic chatbot

I also implement security guardrails to ensure that only I can access and use my assistant safely.

### Key tools and concepts

In this project, I learned several key tools and concepts related to building a persistent AI assistant. I worked with OpenClaw as the main framework and integrated it with Telegram to create a functional chatbot. I learned how to configure the system using workspace files like SOUL.md and USER.md, which define the assistant’s personality and user context. I also understood how memory works in layers, including session memory, daily notes, and long-term storage using state or database systems. Additionally, I explored automation concepts like gateway management, restarting services, and verifying system status. Finally, I learned about security through guardrails, ensuring controlled and safe usage of the assistant.

### Challenges and wins

It was a great hands on project really helped me understand how to build a personalized AI assistant with memory and structure.

---

## Verifying the OpenClaw Setup

In this step, I am making sure that my OpenClaw setup is still working properly before moving forward.

I am confirming that the OpenClaw gateway is running, since it may have stopped if I restarted my computer or closed the terminal. Then, I send a test message on Telegram to verify that my assistant is responding correctly. Finally, I check that my workspace directory exists, so I know everything is set up and ready.

This step ensures I have a stable and working baseline before adding memory and personality to my assistant.

![Image](http://learn.nextwork.org/surprised_maroon_kind_alligator/uploads/ai-openclaw-memory_p3w8n5v2)

---

## Defining a Personality with SOUL.md

In this step, I am giving my OpenClaw assistant a defined personality and identity by creating a SOUL.md file.

In this file, I define things like the assistant’s name, tone, communication style, and behavior rules. OpenClaw reads this file every time it starts, so it directly controls how my assistant speaks and responds. Even small changes in this file can completely change the assistant’s personality, making it feel more unique and aligned with what I want.

After creating the file, I restart the gateway so the new personality is loaded, and then I test it by chatting with my assistant on Telegram.

The reason for this step is to move away from a generic chatbot and create an assistant that feels personal, consistent, and uniquely mine.

![Image](http://learn.nextwork.org/surprised_maroon_kind_alligator/uploads/ai-openclaw-memory_m8t3k6y1)

### How Personality Changes Behavior

The SOUL.md file changes how my assistant behaves by defining its core identity, personality, and communication style. Since OpenClaw reads this file every time the gateway starts, it directly controls how the assistant speaks, responds, and interacts with me in every conversation.

By editing this file, I can move away from a generic chatbot and make my assistant feel more consistent, human-like, and personalized. Even small changes in tone or wording can completely shift how the assistant responds.

In my case, I defined traits such as:

A confident and intelligent tone
Clear, concise, and professional communication
A supportive and proactive attitude, helping me think and solve problems
Slightly friendly and engaging personality so conversations feel natural

This makes my assistant sound less robotic and more like a smart, reliable partner that aligns with my style and goals.

![Image](http://learn.nextwork.org/surprised_maroon_kind_alligator/uploads/ai-openclaw-memory_v5n9b2x7)

---

## Teaching the Assistant About Me

In this step, I am creating a USER.md file to give my assistant context about who I am.

In this file, I add details like my name, preferences, background, and any relevant information I want the assistant to remember. OpenClaw reads this file when the gateway starts, so it allows my assistant to recognize me and personalize its responses instead of treating every conversation like a fresh start.

After creating the file, I restart the gateway so the assistant loads this information, and then I verify it by checking if the assistant greets me by name.

The purpose of this step is to make conversations feel more personal, relevant, and continuous, so my assistant can understand me better and respond in a way that’s tailored to me.

![Image](http://learn.nextwork.org/surprised_maroon_kind_alligator/uploads/ai-openclaw-memory_s3p7q4n9)

### Understanding SOUL.md vs USER.md

The difference between SOUL.md and USER.md is that they define two different sides of the interaction:

SOUL.md defines who the assistant is — its personality, tone, communication style, and behavior. It controls how the assistant speaks and responds.
USER.md defines who I am — my name, preferences, background, and context. It helps the assistant understand me and personalize its responses.

In simple terms, SOUL.md shapes the assistant’s identity, while USER.md provides user context, and together they create a more natural, personalized conversation experience.

---

## Having a Personalized Brainstorm

In this step, I am testing how my assistant automatically builds memory from real conversations.

I have a meaningful conversation with my assistant about my goals, interests, and projects. While I’m chatting, OpenClaw writes daily notes in the background, capturing important details without me needing to manually save anything.

After that, I check the generated daily note file in my workspace to see what information was stored. Then, I start a new conversation to verify that the assistant can remember and use that context, showing that memory persists across sessions.

The purpose of this step is to confirm that my assistant is not just using static files, but is actually learning and evolving over time, creating a continuous and personalized experience.

![Image](http://learn.nextwork.org/surprised_maroon_kind_alligator/uploads/ai-openclaw-memory_u4b3k8w5)

### Three Sources of Context

The three sources of context my assistant draws from when giving personalized recommendations are:

SOUL.md – defines the assistant’s personality, tone, and communication style, which influences how it delivers recommendations.
USER.md – contains information about me, such as my preferences, goals, and background, which helps the assistant tailor recommendations specifically to me.
Automatic daily notes (memory files) – these are created from my conversations and capture ongoing context like my interests, habits, and projects, allowing the assistant to give more accurate and evolving recommendations over time.

![Image](http://learn.nextwork.org/surprised_maroon_kind_alligator/uploads/ai-openclaw-memory_b7m2k9w4)

---

## Exploring Daily Notes and Memory Persistence

OpenClaw’s memory system has four tiers, organized from shortest lived to longest lived. First is Session Memory, which holds temporary context during a single conversation and resets once the session ends. Second is Daily Notes, which automatically capture key points from conversations and persist across sessions, helping the assistant remember recent interactions. Third is Core Memory, stored in workspace files like SOUL.md and USER.md, which define the assistant’s personality and user context and remain consistent over time. Finally, the longest lived is State/Database Memory, stored internally (e.g., SQLite), which keeps structured, long term information about conversations, preferences, and patterns, allowing the assistant to continuously learn and improve.

![Image](http://learn.nextwork.org/surprised_maroon_kind_alligator/uploads/ai-openclaw-memory_y4d5r7j3)

---

## Configuring Security Guardrails

The difference between soft guardrails and hard guardrails in OpenClaw is how strictly they control the assistant’s behavior.

Soft guardrails are flexible guidelines, usually defined in files like SOUL.md. They shape the assistant’s tone, personality, and preferred behavior, but the assistant can still adapt or deviate slightly based on context.
Hard guardrails are strict rules enforced at the system or configuration level. They cannot be bypassed and control things like access, permissions, and security (e.g., allowlists, API limits).

In short, soft guardrails guide behavior, while hard guardrails enforce boundaries.

![Image](http://learn.nextwork.org/surprised_maroon_kind_alligator/uploads/ai-openclaw-memory_w3x7y1z5)

---

## Wrapping Up

It took me approximately 2–3 hours to complete this project, including setup, troubleshooting, and testing the assistant’s memory and personality features.

---

---
