package com.usefulapps.facts

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform