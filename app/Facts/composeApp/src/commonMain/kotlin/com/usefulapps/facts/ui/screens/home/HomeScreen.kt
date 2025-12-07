package com.usefulapps.facts.ui.screens.home

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import org.jetbrains.compose.ui.tooling.preview.Preview

@Composable
@Preview(showBackground = true)
fun HomeScreen(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel
) {
    Column(
        modifier = modifier.padding(8.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        FieldAndButton(
            fieldEnabled = viewModel.inputFieldEnabled.value,
            buttonEnabled = viewModel.buttonEnabled.value,
            setInformation = {viewModel.setInformation("")},
            check = {viewModel.check()}
        )
        if(viewModel.loading.value) Loading()
        if(viewModel.showResults.value) Results()
    }
}

@Composable
@Preview(showBackground = true)
fun FieldAndButton(
    modifier: Modifier = Modifier,
    fieldEnabled: Boolean = true,
    buttonEnabled: Boolean = true,
    setInformation: (String) -> Unit,
    check: () -> Unit
) {
    var text by remember { mutableStateOf("") }
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        OutlinedTextField(
            modifier = Modifier.padding(4.dp),
            value = text,
            onValueChange = {
                text = it
                setInformation(it)
            },
            label = {Text("URL / Fact")},
            enabled = fieldEnabled
        )

        Button(
            modifier = Modifier.padding(8.dp),
            onClick = {
                check()
            },
            enabled = buttonEnabled
        ) {
            Text(text = "Check")
        }
    }
}


@Composable
@Preview(showBackground = true)
fun Loading(
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        CircularProgressIndicator()
    }
}

@Composable
@Preview(showBackground = true)
fun Results(
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
    ) {
        Text("Results")
    }
}