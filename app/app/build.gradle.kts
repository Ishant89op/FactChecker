plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.compose)
    kotlin("plugin.serialization") version "1.9.22"
}

android {
    namespace = "com.usefulapps.factchecker"
    compileSdk {
        version = release(36)
    }

    defaultConfig {
        applicationId = "com.usefulapps.factchecker"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.graphics)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)

    // Ktor Client Core
    implementation(libs.ktor.client.core)
    // for android
    implementation(libs.ktor.client.android)

    // Ktor OkHttp Engine
    implementation(libs.ktor.client.okhttp)

    // Ktor Content Negotiation
    implementation(libs.ktor.client.content.negotiation)

    // Ktor Serialization JSON
    implementation(libs.ktor.serialization.kotlinx.json)

    // Kotlinx Serialization JSON (core library)
    implementation(libs.kotlinx.serialization.json)

    // Google Fonts Library
    implementation(libs.androidx.compose.ui.text.google.fonts)

    // Koin for Android
    implementation(libs.koin.android)

    // Koin for Compose
    implementation(libs.koin.androidx.compose)

    // Koin for Navigation
    implementation(libs.koin.androidx.navigation)


    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.compose.ui.test.junit4)
    debugImplementation(libs.androidx.compose.ui.tooling)
    debugImplementation(libs.androidx.compose.ui.test.manifest)
}