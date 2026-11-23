import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(process.cwd());
const packageJson = JSON.parse(await readFile(resolve(root, "package.json"), "utf8"));
const version = (process.env.SANAD_BUILD_VERSION || packageJson.version).replace(/^v/, "");
const commit = process.env.GITHUB_SHA || process.env.SANAD_BUILD_COMMIT || "local";
const payload = {
    version,
    commit: commit.slice(0, 12),
    builtAt: new Date().toISOString(),
};

await writeFile(
    resolve(root, "public/version.json"),
    `${JSON.stringify(payload, null, 2)}\n`,
    "utf8",
);
console.log(`SANAD build ${payload.version} (${payload.commit})`);
