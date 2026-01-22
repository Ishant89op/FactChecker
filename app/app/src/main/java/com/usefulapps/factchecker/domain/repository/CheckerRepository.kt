package com.usefulapps.factchecker.domain.repository

import com.usefulapps.factchecker.constant.*
import com.usefulapps.factchecker.data.remote.ApiService
import com.usefulapps.factchecker.domain.model.VerifiedResult

class CheckerRepository(
    private val apiService: ApiService
) {

    suspend fun isServiceOnline(): Boolean {
        println(try_api_checkerRepo)
        val response = apiService.runServiceAPI()
        println(response_api_checkerRepo)
        return response.online
    }

    suspend fun verifier(text: String): VerifiedResult {
        println(request_repo_checkerRepo)
        val response = apiService.runVerifierAPI(text)
        println(response_api_checkerRepo)
        return VerifiedResult(
            success = response.success,
            found_on = response.found_on,
            total_checked = response.total_checked,
            results = response.results,
            overall_verdict = response.overall_verdict,
            error = response.error
        )
    }

    suspend fun getInfo(text: String): VerifiedResult {
        println(request_repo_checkerRepo)
        val response = apiService.runGetInfoAPI(text)
        println(response_api_checkerRepo)
        return VerifiedResult(
            success = response.success,
            found_on = response.found_on,
            total_checked = response.total_checked,
            results = response.results,
            overall_verdict = response.overall_verdict,
            error = response.error
        )
    }
}