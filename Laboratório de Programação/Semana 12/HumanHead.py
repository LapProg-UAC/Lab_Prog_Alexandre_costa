import os
import numpy as np
import imageio
import mitsuba as mi

# ── Point Mitsuba to the LLVM library (if needed) ──
llvm_path = "/opt/homebrew/opt/llvm/lib/libLLVM.dylib"
if os.path.exists(llvm_path):
    os.environ['DRJIT_LIBLLVM_PATH'] = llvm_path

mi.set_variant('scalar_rgb')

MODEL_PATH = "UV.obj"
OUTPUT_GIF = "human_head_skin_3_camadas_final.gif"
N_FRAMES = 20

def render_frame(angle_deg):
    rad = np.deg2rad(angle_deg)
    radius = 7.5
    cam_x = radius * np.sin(rad)
    cam_z = radius * np.cos(rad)

    scene_dict = {
        'type': 'scene',

        # ── Integrator ──────────────────────────────────────────────────────────
        # 'path' is faster and more stable than 'volpath' for surface shading.
        # max_depth 8 gives nice indirect bounces without being too slow.
        'integrator': {
            'type': 'path',
            'max_depth': 8
        },

        # ── Camera ──────────────────────────────────────────────────────────────
        'sensor': {
            'type': 'perspective',
            'fov': 40,
            'to_world': mi.scalar_rgb.Transform4f.look_at(
                origin=[cam_x, 2.0, cam_z],
                target=[0, 0, 0],
                up=[0, -1, 0]          # keep original orientation (model Y-flip)
            ),
            'film': {
                'type': 'hdrfilm',
                'width': 600, 'height': 600,
                'pixel_format': 'rgba',
                'rfilter': {'type': 'gaussian'}
            },
            # 512 spp: clean result without a massive render time
            'sampler': {'type': 'independent', 'sample_count': 512}
        },

        # ── Head mesh ───────────────────────────────────────────────────────────
        'head_mesh': {
            'type': 'obj',
            'filename': MODEL_PATH,
            'bsdf': {
                'type': 'blendbsdf',
                # Aumentamos o peso da superfície para 0.35 (era 0.20)
                # Isso define um tom de pele mais neutro e visível na superfície.
                'weight': 0.35,
                
                # CAMADA 1: EPIDERME (Superfície - Tom Bege Neutro)
                # [240, 210, 180] -> [0.94, 0.82, 0.70]
                'bsdf_1': {
                    'type': 'roughplastic',
                    'diffuse_reflectance': {'type': 'rgb', 'value': [0.94, 0.82, 0.70]},
                    'alpha': 0.45,       # Ligeiramente mais matte para suavizar brilhos
                    'int_ior': 1.4
                },
                
                # MISTURA PARA AS CAMADAS INTERNAS (Subsuperfície)
                'bsdf_0': {
                    'type': 'blendbsdf',
                    'weight': 0.65,      # A Derme (rosa) domina a Hipoderme (neutra)
                    
                    # CAMADA 2: DERME (Rosa Suave - para translucidez)
                    # [230, 150, 150] -> [0.90, 0.58, 0.58]
                    'bsdf_1': {
                        'type': 'diffuse',
                        'reflectance': {'type': 'rgb', 'value': [0.90, 0.58, 0.58]}
                    },
                    
                    # CAMADA 3: HIPODERME/BASE (Tom Neutro Claro - substitui o amarelo)
                    # Usamos um bege muito claro e neutro em vez de amarelo puro.
                    # [245, 240, 225] -> [0.96, 0.94, 0.88]
                    'bsdf_0': {
                        'type': 'diffuse',
                        'reflectance': {'type': 'rgb', 'value': [0.96, 0.94, 0.88]}
                    }
                }
            }
        },

        # ── Lighting ────────────────────────────────────────────────────────────
        # Three-point setup: key (warm), fill (neutral), rim (cool back-light).
        # Lights are fixed in world space so the head rotates through them.

        # Key light — warm, slightly above and to the side
        'key_light': {
            'type': 'point',
            'position': [6, 8, 5],
            'intensity': {'type': 'rgb', 'value': [950, 780, 600]}
        },
        # Fill light — cooler, from opposite side, softer
        'fill_light': {
            'type': 'point',
            'position': [-5, 3, 2],
            'intensity': {'type': 'rgb', 'value': [180, 170, 200]}
        },
        # Rim / back light — separates head from background, adds depth
        'rim_light': {
            'type': 'point',
            'position': [0, 4, -9],
            'intensity': {'type': 'rgb', 'value': [320, 260, 210]}
        },
        # Soft ambient bounce — stops the shadowed side going pitch black
        'ambient_light': {
            'type': 'point',
            'position': [0, -6, 0],
            'intensity': {'type': 'rgb', 'value': [80, 70, 65]}
        }
    }

    scene = mi.load_dict(scene_dict)
    return mi.render(scene)


# ── Main render loop ─────────────────────────────────────────────────────────
frames = []
print("Rendering… 2-layer translucent skin, smooth normals, cyan BG.")

for i in range(N_FRAMES):
    angle = (i / N_FRAMES) * 360
    print(f"Frame {i+1}/{N_FRAMES}  (angle = {angle:.1f}°) …")

    image_data = render_frame(angle)
    img_np = np.array(image_data)           # (H, W, 4)  RGBA float

    rgb   = img_np[..., :3].copy()
    alpha = img_np[..., 3] if img_np.ndim == 3 and img_np.shape[2] == 4 \
            else np.ones(img_np.shape[:2], dtype=np.float32)

    # ── Filmic tone-mapping ────────────────────────────────────────────────
    # Reinhard on luminance keeps colours from blowing out while staying warm.
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    lum_mapped = lum / (lum + 1.0 + 1e-6)
    scale = np.where(lum > 1e-6, lum_mapped / (lum + 1e-6), 1.0)[..., np.newaxis]
    rgb = np.clip(rgb * scale, 0, 1)
    # Gamma 2.2 → sRGB
    rgb = np.clip(rgb ** (1.0 / 2.2), 0, 1)

    # ── Cyan background via alpha composite ───────────────────────────────
    # Pure cyan = (0, 1, 1).  Feel free to soften to (0.05, 0.85, 0.85).
    cyan = np.array([0.0, 0.85, 0.85], dtype=np.float32)
    bg_mask = alpha < 0.5
    rgb[bg_mask] = cyan

    frames.append((rgb * 255).astype(np.uint8))

# loop=0 → loops forever in most viewers
imageio.mimsave(OUTPUT_GIF, frames, fps=10, loop=0)
print(f"✓ Done!  Saved to {OUTPUT_GIF}")