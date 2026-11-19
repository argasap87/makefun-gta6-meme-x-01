// gta6-meme-x-01 entry: the program's whole job is to hand the house
// the post's address. POST.json at the repository root names the X post
// (https://x.com/<handle>/status/<id>); this file copies it to the
// grader's output directory so the gate can read it and fetch the post
// itself. The meme is the post: its first picture plus its text are what
// the judge ranks. Nothing written here is judged.
//
// Runs on Node 22 with the standard library only. No network, no wall
// clock, no files outside the repository, so both grading runs write
// the same bytes. Local check:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

// Outside the grader these two stand in for /bot and /output.
const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const post = JSON.parse(readFileSync(join(botDir, "POST.json"), "utf8"));
if (typeof post !== "object" || post === null || typeof post.url !== "string") {
  console.error("POST.json must be a JSON object with a string url field");
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, "POST.json"), JSON.stringify(post) + "\n");
