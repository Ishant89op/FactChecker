package com.usefulapps.factchecker.viewmodel

import androidx.lifecycle.ViewModel
import com.usefulapps.factchecker.constant.*
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
): ViewModel() {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState

    fun setInput(value: String) {
        _uiState.update {
            it.copy(input = value)
        }
    }

    fun check() {
        println(check_function_homeViewmodel)
        val text = _uiState.value.input
        if (text.isBlank()) return

        println(coroutine_homeViewmodel)
        scope.launch {
            println(coroutine_launched_homeViewmodel)
            _uiState.update {
                println(updating_uiState_homeViewmodel)
                it.copy(
                    isLoading = true,
                    isInputEnabled = false,
                    isCheckButtonEnabled = false,
                    isGetInfoButtonEnabled = false,
                    showResults = false
                )
            }

            try {
                println("$call_repo_fn_homeViewmodel$text")
                val verified = repository.verifier(text)
                println(output_repo_homeViewmodel)
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
        println(getInfo_function_homeViewmodel)
        val text = _uiState.value.input
        if (text.isBlank()) return

        println(coroutine_homeViewmodel)
        scope.launch {
            println(coroutine_launched_homeViewmodel)
            _uiState.update {
                println(updating_uiState_homeViewmodel)
                it.copy(
                    isLoading = true,
                    isInputEnabled = false,
                    isCheckButtonEnabled = false,
                    isGetInfoButtonEnabled = false,
                    showResults = false
                )
            }

            try {
                println("$call_repo_fn_homeViewmodel${text}")
                val verified = repository.getInfo(text)
                println(output_repo_homeViewmodel)
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