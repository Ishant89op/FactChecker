package com.usefulapps.factchecker.viewmodel

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
) {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState

    fun setInput(value: String) {
        _uiState.update {
            it.copy(input = value)
        }
    }

    fun check() {
        println("Check fn called")
        val text = _uiState.value.input
        if (text.isBlank()) return

        println("Launching Coroutine")
        scope.launch {
            println("Coroutine Launched")
            _uiState.update {
                println("Updating _uiState")
                it.copy(
                    isLoading = true,
                    isInputEnabled = false,
                    isCheckButtonEnabled = false,
                    isGetInfoButtonEnabled = false,
                    showResults = false
                )
            }

            try {
                println("Calling Repo fn with text = ${text}")
                val verified = repository.verifier(text)
                println("Got Output from Repo")
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        isInputEnabled = true,
                        isCheckButtonEnabled = true,
                        isGetInfoButtonEnabled = true,
                        showResults = true,
                        results = verified.results,
                        error = verified.error
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        isInputEnabled = true,
                        isCheckButtonEnabled = true,
                        showResults = true,
                        results = null
                    )
                }
            }
        }
    }

    fun getInfo() {
        println("Check fn called")
        val text = _uiState.value.input
        if (text.isBlank()) return

        println("Launching Coroutine")
        scope.launch {
            println("Coroutine Launched")
            _uiState.update {
                println("Updating _uiState")
                it.copy(
                    isLoading = true,
                    isInputEnabled = false,
                    isCheckButtonEnabled = false,
                    isGetInfoButtonEnabled = false,
                    showResults = false
                )
            }

            try {
                println("Calling Repo fn with text = ${text}")
                val verified = repository.getInfo(text)
                println("Got Output from Repo")
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        isInputEnabled = true,
                        isCheckButtonEnabled = true,
                        isGetInfoButtonEnabled = true,
                        showResults = true,
                        results = verified.results,
                        error = verified.error
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        isInputEnabled = true,
                        isCheckButtonEnabled = true,
                        showResults = true,
                        results = null
                    )
                }
            }
        }
    }
}