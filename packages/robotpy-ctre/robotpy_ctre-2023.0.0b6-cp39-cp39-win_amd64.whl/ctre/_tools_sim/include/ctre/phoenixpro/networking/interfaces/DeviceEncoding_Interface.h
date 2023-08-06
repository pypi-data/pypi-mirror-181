/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/Context.h"
#include "ctre/phoenix/export.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif
    CTREXPORT int c_ctre_phoenixpro_encode_device(Context context, int deviceId, const char *model, uint32_t *deviceEncoding);
#ifdef __cplusplus
}
#endif
