/******************************************************************************
 * Copyright (c) 2011-2021, NVIDIA CORPORATION.  All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the NVIDIA CORPORATION nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL NVIDIA CORPORATION BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 ******************************************************************************/

#include <cuda_fp16.h>
#include <cuda_bf16.h>

#include "static_switch.h"
#include "fp16_switch.h"
#include "fmha.h"
#include "fmha_fprop_kernel_1xN.h"

void run_fmha_fp16_sm80(Launch_params<FMHA_fprop_params> &launch_params) {
    // FP16_SWITCH(launch_params.params.is_bf16, [&] {
    //     auto dprops = at::cuda::getCurrentDeviceProperties();
    //     if (launch_params.params.d <= 32) {
    //         if (launch_params.params.seqlen_k == 128) {
    //             using Kernel_traits = FMHA_kernel_traits<128, 32, 16, 1, 4, 0x08u, elem_type>;
    //             run_fmha_fp16_sm80_loop_<Kernel_traits>(launch_params);
    //         } else if (launch_params.params.seqlen_k >= 256) {
    //             using Kernel_traits = FMHA_kernel_traits<256, 32, 16, 1, 4, 0x08u, elem_type>;
    //             run_fmha_fp16_sm80_loop_<Kernel_traits>(launch_params);
    //         }
    //     } else if (launch_params.params.d <= 64) {
    //         if (launch_params.params.seqlen_k == 128) {
    //             using Kernel_traits = FMHA_kernel_traits<128, 64, 16, 1, 4, 0x08u, elem_type>;
    //             run_fmha_fp16_sm80_loop_<Kernel_traits>(launch_params);
    //         } else if (launch_params.params.seqlen_k >= 256) {
    //             using Kernel_traits = FMHA_kernel_traits<256, 64, 16, 1, 4, 0x08u, elem_type>;
    //             run_fmha_fp16_sm80_loop_<Kernel_traits>(launch_params);
    //         }
    //     } else if (launch_params.params.d <= 128) {
    //         // TD [2022-10-21]: Previously for SM80 we use block size 256 and keep K in shared memory
    //         // to reduce register spilling. However, that increases the smem usage from ~41KB to ~105KB,
    //         // reducing occupancy (only 1 kernel can be scheduled per SM instead of 2). This strategy gives
    //         // some speedup (6-10%) for large batch size, but slows things down for smal batch size.
    //         // Now that we have better parallelism (over seqlen_q), block size 128 is faster for small
    //         // batch size and only slightly slower (~3%) on large batch size.
    //         // For causal=True, block size 128 seems always faster (for small & large batch size).
    //         // So we're just gonna use block size 128 for simplicity.
    //         using Kernel_traits = FMHA_kernel_traits<128, 128, 16, 1, 4, 0x08u, elem_type>;
    //         run_fmha_fp16_sm80_loop_<Kernel_traits>(launch_params);
    //     }
    //     // if (launch_params.params.d == 64) {
    //     //     // using Kernel_traits = FMHA_kernel_traits<128, 64, 16, 1, 4, 0x08u, elem_type>;
    //     //     // using Kernel_traits = FMHA_kernel_traits<64, 64, 16, 1, 4, 0x08u, elem_type>;
    //     //     // using Kernel_traits = FMHA_kernel_traits<512, 64, 16, 1, 8, 0x08u, elem_type>;
    //     //     using Kernel_traits = FMHA_kernel_traits<128, 64, 16, 1, 4, 0x08u, elem_type>;
    //     //     run_fmha_fp16_sm80_loop_<Kernel_traits>(launch_params);
    //     // }
    // });
    if (launch_params.params.d <= 32) {
        run_fmha_fwd_hdim32(launch_params);
    } else if (launch_params.params.d <= 64) {
        run_fmha_fwd_hdim64(launch_params);
    } else if (launch_params.params.d <= 128) {
        run_fmha_fwd_hdim128(launch_params);
    }
}