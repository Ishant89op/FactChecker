package com.usefulapps.factchecker.domain.repository

import com.usefulapps.factchecker.data.remote.ApiService
import com.usefulapps.factchecker.domain.model.VerifiedResult

class CheckerRepository(
    private val apiService: ApiService
) {

    suspend fun isServiceOnline(): Boolean {
        println("Trying to get API.")
        val response = apiService.runServiceAPI()
        println("Got response from API")
        return response.online
    }

    suspend fun verifier(text: String): VerifiedResult {
        println("Request reached Repository")
        val response = apiService.runVerifierAPI(text)
        println("Got Output from API")
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
        println("Request reached Repository")
        val response = apiService.runGetInfoAPI(text)
        println("Got Output from API")
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