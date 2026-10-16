# Motion reference, skeleton reasoning and proportion-aware adaptation

Use this stage for a new or substantially redesigned action. An edge-only repair with a clear source does not require repeating unrelated research. Keep research bounded to the requested action, not a broad inspiration dump.

## Observe, then design

1. Search public web references for the actual action/intent: palm-launched projectile versus physical throwing, guarded cast versus broad ritual motion, grounded jump versus float. Pixel animation is useful for pixel timing; live-action, drawn animation and 3D game motion can reveal weight and arcs.
2. Prefer original artist/developer/educator sources. Inspect accessible source visuals or timestamped footage. Record URL, author, access date, what was actually viewed and limitations. A search snippet, article description or video title is not observed movement. If a video cannot be viewed, choose accessible frames/another source or mark that portion incomplete.
3. When permitted by access/rights, use a local clip or frame sequence for measurement. Do not circumvent access controls, install unknown downloaders or redistribute tutorial/game media in the final pack. Store derived notes, links and your own abstract landmark sketches instead. Do not upload private character art to an analysis site without permission.
4. Identify reference qualities to borrow, not an exact proprietary character design. Save a concise motion study: phase times, line of action, contacts, joint paths, depth transitions, driver/follower relationships and intended adaptation.

## Study representation

For each useful key moment record:

- source timestamp or frame and time base; note unknown timing rather than guess;
- pelvis/root, chest/head orientation, shoulder/elbow/wrist and hip/knee/ankle landmarks where applicable;
- support foot/contact interval, contact hand/prop and grounded/airborne state;
- line of action, direction of force and broad mass distribution;
- hand/foot/appendage path with occluded landmarks labeled inferred;
- preparation, drive, release/contact, extension, recovery and settle events;
- slow holds versus fast accents, approximate spacing, secondary lag and loop/non-loop intent.

Camera movement and perspective can change screen-space trajectories without changing body motion. Estimate them separately or document uncertainty. Avoid declaring physical speed from uncalibrated pixels.

## Available skeleton aids

Manual 2D landmarks and a drawn wireframe are the baseline and work for stylized/nonhuman characters. If an appropriate pose estimator already exists, treat its landmarks and confidence as proposals, not anatomy truth; hands, skirts, tails and occlusion often need manual correction. Do not claim automatic extraction from a manually placed rig.

A project-local Blender armature/IK proxy can test reach, limb length, support, depth and overlap. It is optional, not a required detour for a simple sprite. Prior experiments used a local headless proxy, not full mocap or physics. Keep source landmarks and target rig parameters separate. Read [tool-adapters.md](tool-adapters.md) before configuring tools.

## Retarget to this character

Measure target proportions from the accepted references: head/body, torso, upper/lower limb, shoulder/hip width and appendage roots. Normalize source landmarks to a meaningful body scale, then construct the target using its own segment lengths. Do not copy raw source pixel coordinates or joint angles blindly.

Preserve the action's purpose, event ordering and contact constraints. Re-solve end-effector reach and joint bend. A large head/short arm may require torso lean, a different elbow path, step or smaller amplitude; long arms may need increased clearance. Adjust foot placement/pelvis height to keep planted contacts believable. Use foreshortening/occlusion for depth, not unexplained shortening. Different proportions can justify different timing and balance, but do not automatically make every small character fast.

## Physical plausibility with deliberate stylization

Check support/center-of-mass plausibility, planted feet, inertia, acceleration/deceleration, force/reaction, collision clearance, cloth lag and recovery. Airborne characters need a coherent intended arc or an explicit magical mechanism. A fireball separates at release and moves independently afterward; a palm cast need not use a lob trajectory. Passive cloth should not lead its driver without a cause; an actively controlled tail may lead intentionally.

These are visual/kinematic judgments, not a physical simulation certificate. Document deliberate stylization, overshoot or smear rather than enforcing realism that contradicts the brief. Revise impossible reach/contact before adding texture/FX.

## Output gate

Produce an original action plan with chosen sources, observed evidence/limits, key-pose sketches or proxy, event timeline and character-specific adaptation notes. No fixed drawing count or universal phase ratio. Review the blocked action without effects before detailed rendering. If web access or playback is unavailable, preserve a provisional plan with the incomplete gate disclosed, not invented research.
