package com.usefulapps.factchecker.viewmodel.model

import com.usefulapps.factchecker.data.model.HistoryItem
import com.usefulapps.factchecker.domain.model.VerifiedResult

data class HomeUiState(
    val input: String = "",
    val isLoading: Boolean = false,
    val isInputEnabled: Boolean = true,
    val isServerOnline: Boolean = true,
    val showResults: Boolean = false,
    val result: VerifiedResult? = null,
    val error: String? = null,
    // Loading screen state
    val currentStatus: String = "",
    val statusMessage: String = "",
    val sourcesChecked: Int = 0,
    // History
    val history: List<HistoryItem> = emptyList(),
    val historyCursor: String = "",
    val isLoadingHistory: Boolean = false
)
