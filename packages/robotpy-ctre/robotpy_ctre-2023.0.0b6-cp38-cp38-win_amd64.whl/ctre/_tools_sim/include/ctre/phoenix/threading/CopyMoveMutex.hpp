/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include <mutex>

namespace ctre {
namespace phoenix {
namespace threading {

	/**
	 * \brief An extension of mutex that defines empty copy and
	 * move constructors and assignment operators.
	 *
	 * \details This allows classes using a #CopyMoveMutex to have copy and move semantics.
	 */
	template <class MutexType>
	class CopyMoveMutex : public MutexType {
	public:
		CopyMoveMutex() = default;
		CopyMoveMutex(CopyMoveMutex const &) : CopyMoveMutex{} {}
		CopyMoveMutex(CopyMoveMutex &&) : CopyMoveMutex{} {}
		CopyMoveMutex &operator=(CopyMoveMutex const &) { return *this; }
		CopyMoveMutex &operator=(CopyMoveMutex &&) { return *this; }
	};

}
}
}
