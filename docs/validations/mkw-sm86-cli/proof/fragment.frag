#version 460
#extension GL_ARB_gpu_shader_int64 : require
#define LOOP_CAP 0x1000u
layout(location = 0) in vec4 in_attr0;
layout(location = 0) out vec4 out_color0;
void main() {
    precise uint r0 = 0u, r1 = 0u, r2 = 0u, r3 = 0u;
    bool p0 = false, p1 = false, p2 = false, p3 = false, p4 = false, p5 = false, p6 = false, up0 = false, up1 = false, up2 = false, up3 = false, up4 = false, up5 = false, up6 = false;
    uint loops = 0u;
        r0 = floatBitsToUint((in_attr0[0] * gl_FragCoord.w));
        r1 = floatBitsToUint((in_attr0[1] * gl_FragCoord.w));
        r2 = floatBitsToUint((in_attr0[2] * gl_FragCoord.w));
        r3 = floatBitsToUint((in_attr0[3] * gl_FragCoord.w));
        r0 = floatBitsToUint((uintBitsToFloat(r0) + uintBitsToFloat(r1)));
        out_color0[0] = uintBitsToFloat(r0); out_color0[1] = uintBitsToFloat(r1); out_color0[2] = uintBitsToFloat(r2); out_color0[3] = uintBitsToFloat(r3); return;
}
