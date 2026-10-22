# Request traceability

| User requirement | Implementation | Verification |
| --- | --- | --- |
| Full pipeline, arbitrary entry | SKILL + stages-and-entry + project record (resume-or-new) | Field test entering at views from a pixel image |
| Text / ordinary / pixel references | character-design input branches | Text smoke test; other branches documented |
| Pixel grid set by the reference (user size, otherwise a 256×256 canvas); canvas follows the action; export is an integer scale (Scale2x by default, nearest neighbor on request) | entrypoint rule, pixel-scale reference, existing-project rule | Field-test dimensions; the owner's scale definition (2026-10-22) |
| Natural outlines, color and per-frame detail; compressing and adding detail | pixel-art-spec, motion-design (rig cleanup, effect construction), pixel-scale | Research pass with experiments on the field-test character (outside this repository) |
| Image generation / Codex / selected provider | tool-adapters capability and permission branches | Local discovery/help + adapter dry-run; live external APIs not tested |
| Multi-view refs, clean edges/palette, identity | character-design + pixel-art-spec + visual gates | Primary tutorial research; actual universal multiview success not claimed |
| Unlimited action frames, rhythm | motion-design and no fixed drawing cap | Existing exporter timing regressions; new-action generalization not claimed |
| Online reference research | motion-research with observation/evidence/rights boundaries | Primary sources investigated; execution requires actual accessible motion media |
| Skeleton and proportion adaptation | manual landmarks, optional verified Blender/IK aid | Prior real tool experience + version/help inspection; not mocap/physics proof |
| Per-frame identity/dirt/edge/continuity fixes | every-authored-frame gate, local edge-diff + actual playback | Retained bridge/export tests; technical results not naturalness scores |
| Useful tools, local-only config | Aseprite MCP stdio, CLI, Blender, local venv/templates | Version/help/source checks, templates parsed; no global install |
| Mature skill/spec designs | research-lineage + RESEARCH.md adoption/rejection log | Eight public source skills inspected; no copied implementation |
| Maintainable, publishable repository | README with install commands, MIT license, marketplace entry, changelog, tests | Unit tests, repository validation, `claude plugin validate` |
