---
type: technical_standard
target_engine: Godot 4.7, Unity 6, Vulkan
status: verified
---

# 🛠️ Agent Skill: Shader Development

## Purpose
This skill provides production-ready standards for writing GPU shaders in Godot 4.7 (GDShader) and Vulkan. It ensures optimal performance on mid-range hardware (RTX 4060 8GB VRAM).

---

## 📐 GDShader Standards (Godot 4.7)

### Mandatory Declarations
In Godot 4.x, screen and depth textures are **NOT** built-in globals. Always declare them explicitly:
```glsl
uniform sampler2D SCREEN_TEXTURE : hint_screen_texture, filter_linear_mipmap;
uniform sampler2D DEPTH_TEXTURE : hint_depth_texture, filter_linear_mipmap;
```

### Render Mode Guidelines
| Effect | Recommended Render Mode |
|---|---|
| Water (stylized) | `depth_draw_always, cull_back, specular_schlick_ggx, diffuse_lambert_wrap` |
| Lava (emissive) | `depth_draw_opaque, cull_back, unshaded` |
| Glass (transparent) | `depth_draw_always, cull_disabled, blend_mix` |
| Foliage (alpha-cutout) | `depth_draw_opaque, cull_disabled, specular_schlick_ggx` |

### Invalid Render Modes (Common Errors)
- ❌ `diffused_light` — Does not exist. Use `diffuse_lambert_wrap` or `diffuse_burley`.
- ❌ `DEPTH_TEXTURE` as built-in — Must be declared as `uniform sampler2D`.

---

## ⚡ Performance Optimization (RTX 4060)

### Fragment Shader Budget
- **Avoid** procedural `fbm()` (4+ octave noise) per pixel on high-subdivision meshes.
- **Prefer** pre-generated `NoiseTexture2D` (FastNoiseLite) passed as `sampler2D` uniforms.
- **Target**: < 50 instruction count per fragment for 60fps at 128x128 subdivision.

### Vertex Shader Budget
- Use sine wave layering (3 waves max) for vertex displacement.
- Avoid `texture()` calls in vertex shaders — use math-only displacement.

### Mesh Settings
- Water/Lava: `PlaneMesh` subdivided at **128x128** max.
- Terrain: LOD mesh with 2-3 levels (far: 200 tris, close: 1000 tris).

---

## 🔥 Proven Shader Patterns

### Cross-Learning Pipeline
When creating a new shader, always check `memory/` for existing verified shaders to reuse:
1. **Noise functions** (`hash`, `noise`, `fbm`) — reusable across all procedural shaders.
2. **Vertex wave displacement** — reusable for water, lava, wind, fabric.
3. **Depth-based effects** — reusable for fog, transparency, foam.

### Reference Shaders
- `memory/SHADER_WATER.md` — Stylized Water (foam, refraction, depth transparency).
- Lava Shader — Derived from Water via Cross-Learning (Magma Crust + Voronoi + Emission).

---

## 🧪 Shader Validation Checklist
```
1. Does the shader compile without errors in Godot 4.7?
2. Are SCREEN_TEXTURE and DEPTH_TEXTURE explicitly declared?
3. Is the render mode valid (no typos like 'diffused_light')?
4. Does it maintain 60fps at 128x128 mesh subdivision on RTX 4060?
5. Are all @export uniforms properly typed and grouped?
```
