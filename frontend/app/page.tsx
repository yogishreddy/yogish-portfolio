"use client";

import { useState } from "react";

import { profile } from "../data/profile";
import { experience } from "../data/experience";
import { projects } from "../data/projects";
import { skills } from "../data/skills";

export default function Home() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  type Message = {
    role: "user" | "assistant";
    content: string;
  };

  const [messages, setMessages] = useState<Message[]>([]);

  const [sources, setSources] = useState<
    { title: string; similarity: number }[]
  >([]);

  const askAI = async () => {
    if (!message.trim() || loading) {
      return;
    }

    const userMessage = message;

    setLoading(true);
    setSources([]);

    // Add the user's message immediately.
    // Add an empty assistant message that will be filled while streaming.
    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userMessage,
      },
      {
        role: "assistant",
        content: "",
      },
    ]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
          history: messages,
        }),
      });

      if (!res.ok) {
        throw new Error(`Backend returned ${res.status}`);
      }

      const reader = res.body?.getReader();

      if (!reader) {
        throw new Error("Streaming is not supported");
      }

      const decoder = new TextDecoder();

      let buffer = "";
      let fullResponse = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");

        // Keep an incomplete JSON line for the next network chunk.
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.trim()) {
            continue;
          }

          const data = JSON.parse(line);

          if (data.type === "token") {
            fullResponse += data.content;

            setMessages((previous) => {
              const updated = [...previous];

              // The last message is the assistant message
              // currently being streamed.
              updated[updated.length - 1] = {
                role: "assistant",
                content: fullResponse,
              };

              return updated;
            });
          }

          if (data.type === "sources") {
            setSources(data.sources);
          }

          if (data.type === "done") {
            console.log("Streaming complete");
          }
        }
      }

      // Process any remaining buffered line.
      if (buffer.trim()) {
        const data = JSON.parse(buffer);

        if (data.type === "token") {
          fullResponse += data.content;

          setMessages((previous) => {
            const updated = [...previous];

            updated[updated.length - 1] = {
              role: "assistant",
              content: fullResponse,
            };

            return updated;
          });
        }

        if (data.type === "sources") {
          setSources(data.sources);
        }
      }

      setMessage("");
    } catch (error) {
      console.error(error);

      setMessages((previous) => {
        const updated = [...previous];

        updated[updated.length - 1] = {
          role: "assistant",
          content: "Unable to connect to the AI backend.",
        };

        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 border-b border-zinc-900/80 bg-black/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <a
            href="#"
            className="text-lg font-bold tracking-tight"
          >
            {profile.name.toUpperCase()}
          </a>

          <div className="hidden items-center gap-8 text-sm text-zinc-400 md:flex">
            <a
              href="#about"
              className="transition hover:text-white"
            >
              About
            </a>

            <a
              href="#experience"
              className="transition hover:text-white"
            >
              Experience
            </a>

            <a
              href="#projects"
              className="transition hover:text-white"
            >
              Projects
            </a>

            <a
              href="#skills"
              className="transition hover:text-white"
            >
              Skills
            </a>

            <a
              href="#ai"
              className="rounded-full border border-zinc-700 px-4 py-2 text-white transition hover:border-zinc-400"
            >
              Ask My AI
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto flex min-h-[80vh] max-w-6xl flex-col justify-center px-6 py-24">
        <div className="max-w-5xl">
          <p className="mb-6 text-sm font-medium tracking-[0.25em] text-zinc-500">
            CLOUD • DEVOPS • AI ENGINEERING
          </p>

          <h1 className="text-5xl font-bold leading-tight tracking-tight md:text-7xl">
            {profile.tagline}
          </h1>

          <p className="mt-8 max-w-2xl text-lg leading-8 text-zinc-400 md:text-xl">
            {profile.summary}
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <a
              href="#projects"
              className="rounded-lg bg-white px-6 py-3 font-medium text-black transition hover:bg-zinc-200"
            >
              View Projects
            </a>

            <a
              href="#ai"
              className="rounded-lg border border-zinc-700 px-6 py-3 font-medium transition hover:border-zinc-400"
            >
              Ask My AI →
            </a>
          </div>
        </div>

        {/* Focus areas */}
        <div className="mt-20 flex flex-wrap gap-3">
          {profile.focus.map((item) => (
            <span
              key={item}
              className="rounded-full border border-zinc-800 px-4 py-2 text-sm text-zinc-400"
            >
              {item}
            </span>
          ))}
        </div>
      </section>

      {/* About */}
      <section
        id="about"
        className="border-t border-zinc-900"
      >
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm font-medium tracking-[0.2em] text-zinc-500">
            ABOUT
          </p>

          <div className="mt-10 grid gap-12 md:grid-cols-2">
            <div>
              <h2 className="text-3xl font-semibold leading-tight md:text-4xl">
                From infrastructure to intelligent systems.
              </h2>
            </div>

            <div>
              <p className="leading-8 text-zinc-400">
                My background is in cloud infrastructure, CI/CD and DevOps.
                I&apos;m expanding into AI engineering, agentic systems and
                AI-powered platform engineering by building practical,
                production-oriented projects.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Experience */}
      <section
        id="experience"
        className="border-t border-zinc-900"
      >
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm font-medium tracking-[0.2em] text-zinc-500">
            EXPERIENCE
          </p>

          <div className="mt-12 space-y-12">
            {experience.map((item) => (
              <article
                key={`${item.company}-${item.role}`}
                className="border-l border-zinc-800 pl-6"
              >
                <p className="text-sm font-medium tracking-wider text-zinc-500">
                  {item.company.toUpperCase()}
                </p>

                <h2 className="mt-2 text-2xl font-semibold">
                  {item.role}
                </h2>

                <p className="mt-5 max-w-3xl leading-8 text-zinc-400">
                  {item.description}
                </p>

                <div className="mt-6 flex flex-wrap gap-2">
                  {item.technologies.map((technology) => (
                    <span
                      key={technology}
                      className="rounded-full bg-zinc-900 px-3 py-1 text-xs text-zinc-400"
                    >
                      {technology}
                    </span>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* Projects */}
      <section
        id="projects"
        className="border-t border-zinc-900"
      >
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm font-medium tracking-[0.2em] text-zinc-500">
            PROJECTS
          </p>

          <h2 className="mt-4 text-3xl font-semibold md:text-4xl">
            Things I&apos;m building.
          </h2>

          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {projects.map((project) => (
              <article
                key={project.title}
                className="group flex flex-col rounded-2xl border border-zinc-800 p-6 transition duration-300 hover:-translate-y-1 hover:border-zinc-600"
              >
                <div className="flex items-start justify-between gap-4">
                  <h3 className="text-xl font-semibold">
                    {project.title}
                  </h3>

                  <span className="whitespace-nowrap rounded-full bg-zinc-900 px-3 py-1 text-xs text-zinc-500">
                    {project.status}
                  </span>
                </div>

                <p className="mt-5 flex-1 text-sm leading-7 text-zinc-400">
                  {project.description}
                </p>

                <div className="mt-6 flex flex-wrap gap-2">
                  {project.tags.map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full border border-zinc-800 px-3 py-1 text-xs text-zinc-400"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* Skills */}
      <section
        id="skills"
        className="border-t border-zinc-900"
      >
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm font-medium tracking-[0.2em] text-zinc-500">
            TECHNOLOGIES
          </p>

          <div className="mt-12 grid gap-10 md:grid-cols-2">
            {Object.entries(skills).map(([category, items]) => (
              <div key={category}>
                <h3 className="text-lg font-semibold capitalize">
                  {category}
                </h3>

                <div className="mt-4 flex flex-wrap gap-3">
                  {items.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-lg border border-zinc-800 px-4 py-2 text-sm text-zinc-300 transition hover:border-zinc-600"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Assistant */}
      <section
        id="ai"
        className="border-t border-zinc-900"
      >
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm font-medium tracking-[0.2em] text-zinc-500">
            AI ASSISTANT
          </p>

          <div className="mt-10 grid gap-12 md:grid-cols-2">
            {/* Introduction */}
            <div>
              <h2 className="text-3xl font-semibold leading-tight md:text-4xl">
                Ask me anything about my work.
              </h2>

              <p className="mt-6 max-w-lg leading-8 text-zinc-400">
                Ask questions about my experience, projects, skills,
                technologies and technical work.
              </p>
            </div>

            {/* Chat */}
            <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
              <label
                htmlFor="ai-question"
                className="text-sm font-medium text-zinc-300"
              >
                Your question
              </label>

              <div className="mt-4 flex flex-col gap-3 sm:flex-row">
                <input
                  id="ai-question"
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      askAI();
                    }
                  }}
                  placeholder="e.g. What technologies does Yogish know?"
                  className="min-w-0 flex-1 rounded-lg border border-zinc-800 bg-black px-4 py-3 text-sm text-white outline-none placeholder:text-zinc-600 focus:border-zinc-500"
                />

                <button
                  onClick={askAI}
                  disabled={loading}
                  className="rounded-lg bg-white px-5 py-3 text-sm font-medium text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? "Generating..." : "Ask"}
                </button>
              </div>

              {/* Chat messages */}
              {messages.length > 0 && (
                <div className="mt-6 space-y-4">
                  {messages.map((chatMessage, index) => (
                    <div
                      key={index}
                      className={
                        chatMessage.role === "user"
                          ? "flex justify-end"
                          : "flex justify-start"
                      }
                    >
                      <div
                        className={
                          chatMessage.role === "user"
                            ? "max-w-[85%] rounded-2xl bg-white px-4 py-3 text-sm text-black"
                            : "max-w-[85%] rounded-2xl border border-zinc-800 bg-black px-4 py-3 text-sm leading-7 text-zinc-300"
                        }
                      >
                        <p>
                          {chatMessage.content}
                          {loading &&
                            chatMessage.role === "assistant" &&
                            index === messages.length - 1 && (
                              <span className="ml-1 inline-block animate-pulse">
                                ▋
                              </span>
                            )}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Retrieved sources */}
              {sources.length > 0 && (
                <div className="mt-6 border-t border-zinc-800 pt-5">
                  <p className="text-xs font-medium uppercase tracking-wider text-zinc-500">
                    Retrieved sources
                  </p>

                  <div className="mt-3 space-y-2">
                    {sources.map((source) => (
                      <div
                        key={source.title}
                        className="flex items-center justify-between rounded-lg border border-zinc-800 bg-zinc-950 px-4 py-3"
                      >
                        <span className="text-sm text-zinc-300">
                          {source.title}
                        </span>

                        <span className="text-xs text-zinc-500">
                          {(source.similarity * 100).toFixed(1)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-zinc-900">
        <div className="mx-auto max-w-6xl px-6 py-10 text-center text-sm text-zinc-600">
          © {new Date().getFullYear()} {profile.name}. Built with Next.js.
        </div>
      </footer>
    </main>
  );
}