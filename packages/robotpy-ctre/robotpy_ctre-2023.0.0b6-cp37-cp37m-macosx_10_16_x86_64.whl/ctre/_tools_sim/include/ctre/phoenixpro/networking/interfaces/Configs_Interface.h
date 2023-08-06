/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/StatusCodes.h"
#include "ctre/phoenix/export.h"
#include "ctre/phoenixpro/networking/interfaces/DeviceEncoding_Interface.h"
#include <cstdint>
#include <string>

#ifdef __cplusplus
extern "C"
{
#endif

    CTREXPORT int c_ctre_phoenixpro_set_configs(
        Context context,
        const char *network,
        int deviceHash,
        double timeoutSeconds,
        const char *values,
        size_t value_len,
        bool futureProofConfigs,
        bool overrideIfDuplicate,
        bool useDid);

    CTREXPORT int c_ctre_phoenixpro_get_configs(
        Context context,
        const char *network,
        int deviceHash,
        double timeoutSeconds,
        char **str,
        bool useDid);

#ifdef __cplusplus
}
#endif
