#version 460
#extension GL_ARB_gpu_shader_int64 : require
#define LOOP_CAP 0x1000u
layout(location = 0) in vec4 in_attr0;
layout(location = 0) out vec4 out_attr0;
layout(std140, binding = 0) uniform Support { vec4 pad[87]; float point_size; } support;
void main() {
    precise uint r0 = 0u, r1 = 0u, r2 = 0u, r3 = 0u;
    bool p0 = false, p1 = false, p2 = false, p3 = false, p4 = false, p5 = false, p6 = false, up0 = false, up1 = false, up2 = false, up3 = false, up4 = false, up5 = false, up6 = false;
    uint loops = 0u;
    gl_PointSize = support.point_size;
    gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
        r0 = floatBitsToUint(in_attr0[0]); r1 = floatBitsToUint(in_attr0[1]); r2 = floatBitsToUint(in_attr0[2]); r3 = floatBitsToUint(in_attr0[3]);
        r0 = floatBitsToUint((uintBitsToFloat(r0) * uintBitsToFloat(r1)));
        gl_Position[0] = uintBitsToFloat(r0); gl_Position[1] = uintBitsToFloat(r1); gl_Position[2] = uintBitsToFloat(r2); gl_Position[3] = uintBitsToFloat(r3);
        out_attr0[0] = uintBitsToFloat(r0); out_attr0[1] = uintBitsToFloat(r1); out_attr0[2] = uintBitsToFloat(r2); out_attr0[3] = uintBitsToFloat(r3);
        return;
}
