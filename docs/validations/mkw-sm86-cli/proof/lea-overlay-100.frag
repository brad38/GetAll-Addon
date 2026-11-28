#version 460
#extension GL_ARB_gpu_shader_int64 : require
#define LOOP_CAP 0x1000u
layout(location = 0) out vec4 out_color0;
void main() {
    precise uint r0 = 0u, r1 = 0u, r2 = 0u, r3 = 0u;
    bool p0 = false, p1 = false, p2 = false, p3 = false, p4 = false, p5 = false, p6 = false, up0 = false, up1 = false, up2 = false, up3 = false, up4 = false, up5 = false, up6 = false;
    uint loops = 0u;
        { uint lea_shifted = uint(((uint64_t(uint(int(r1) >> 31)) << 32u) | uint64_t(r1)) >> 32u); uint lea_b = r2; bool lea_negcarry = false; lea_b = ~lea_b; bool lea_carry = p0; uint64_t lea_sum = uint64_t(lea_shifted) + uint64_t(lea_b) + uint64_t(lea_carry ? 1u : 0u); r0 = uint(lea_sum); p1 = lea_negcarry || ((lea_sum >> 32u) != uint64_t(0)); }
        out_color0[0] = uintBitsToFloat(r0); out_color0[1] = uintBitsToFloat(r1); out_color0[2] = uintBitsToFloat(r2); out_color0[3] = uintBitsToFloat(r3); return;
}
