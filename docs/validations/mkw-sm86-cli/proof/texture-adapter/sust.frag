#version 460
#extension GL_ARB_gpu_shader_int64 : require
#extension GL_EXT_shader_image_load_formatted : require
#define LOOP_CAP 0x1000u
layout(location = 0) out vec4 out_color0;
layout(binding = 1) uniform image2D i0_88;
void main() {
    precise uint r0 = 0u, r1 = 0u, r2 = 0u, r3 = 0u, r8 = 0u, r9 = 0u, r12 = 0u, r13 = 0u, r14 = 0u, r15 = 0u;
    bool p0 = false, p1 = false, p2 = false, p3 = false, p4 = false, p5 = false, p6 = false, up0 = false, up1 = false, up2 = false, up3 = false, up4 = false, up5 = false, up6 = false;
    uint loops = 0u;
        imageStore(i0_88, ivec2(int(r8), int(r9)), vec4(uintBitsToFloat(r12), uintBitsToFloat(r13), uintBitsToFloat(r14), uintBitsToFloat(r15)));
        out_color0[0] = uintBitsToFloat(r0); out_color0[1] = uintBitsToFloat(r1); out_color0[2] = uintBitsToFloat(r2); out_color0[3] = uintBitsToFloat(r3); return;
}
