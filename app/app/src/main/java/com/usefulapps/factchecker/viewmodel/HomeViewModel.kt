package com.usefulapps.factchecker.viewmodel

import androidx.lifecycle.ViewModel
import com.usefulapps.factchecker.domain.repository.CheckerRepository
import com.usefulapps.factchecker.viewmodel.model.HomeUiState
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class HomeViewModel(
    private val repository: CheckerRepository
) : ViewModel() {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState

    fun setInput(value: String) {
        _uiState.update { it.copy(input = value) }
    }

    fun verify() {
        val text = _uiState.value.input.trim()
        if (text.isBlank()) return

        // Detect if input is a URL
        val inputType = if (text.startsWith("http://") || text.startsWith("https://")) "url" else "statement"

        scope.launch {
            _uiState.update {
                it.copy(
                    isLoading = true,
                    isInputEnabled = false,
                    showResults = false,
                    result = null,
                    error = null,
                    currentStatus = "queued",
                    statusMessage = "Starting verification...",
                    sourcesChecked = 0
                )
            }

            try {
                val result = repository.verify(
                    input = text,
                    type = inputType,
                    onStatusUpdate = { status, message, sourcesChecked ->
                        _uiState.update {
                            it.copy(
                                currentStatus = status,
                                statusMessage = message,
                                sourcesChecked = sourcesChecked
                            )
                        }
                    }
                )

                _uiState.update {
                    it.copy(
                        isLoading = false,
                        isInputEnabled = true,
                        showResults = true,
                        result = result,
                        error = result.error
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        isInputEnabled = true,
                        showResults = false,
                        error = "Connection error: ${e.message?.take(100)}"
                    )
                }
            }
        }
    }

    fun clearResult() {
        _uiState.update {
            it.copy(
                showResults = false,
                result = null,
                error = null,
                input = ""
            )
        }
    }

    fun testServer() {
        scope.launch {
            try {
                val online = repository.isServiceOnline()
                _uiState.update { it.copy(isServerOnline = online) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isServerOnline = false) }
            }
        }
    }

    fun loadHistory() {
        scope.launch {
            _uiState.update { it.copy(isLoadingHistory = true) }
            try {
                val (items, cursor) = repository.getHistory()
                _uiState.update {
                    it.copy(
                        history = items,
                        historyCursor = cursor,
                        isLoadingHistory = false
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoadingHistory = false) }
            }
        }
    }

    fun loadMoreHistory() {
        val cursor = _uiState.value.historyCursor
        if (cursor.isEmpty()) return

        scope.launch {
            try {
                val (items, newCursor) = repository.getHistory(cursor)
                _uiState.update {
                    it.copy(
                        history = it.history + items,
                        historyCursor = newCursor
                    )
                }
            } catch (_: Exception) { }
        }
    }
}