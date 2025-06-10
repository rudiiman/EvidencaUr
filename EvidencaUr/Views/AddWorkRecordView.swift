//
//  AddWorkRecordView.swift
//  EvidencaUr
//
//  Created by Gašper Krajnc on 9. 6. 25.
//

import SwiftUI

struct AddWorkRecordView: View {
    @Environment(\.managedObjectContext) private var viewContext
    @State private var company: String = ""
    @State private var earnings: String = ""
    @State private var startTime = Date()
    @State private var endTime = Date()

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Work Details")) {
                    TextField("Company", text: $company)
                    TextField("Earnings", text: $earnings)
                        .keyboardType(.decimalPad)
                    DatePicker("Start Time", selection: $startTime, displayedComponents: .hourAndMinute)
                    DatePicker("End Time", selection: $endTime, displayedComponents: .hourAndMinute)
                }

                Button(action: saveWorkRecord) {
                    Text("Save Work Record")
                }
            }
            .navigationTitle("Add Work Record")
        }
    }

    private func saveWorkRecord() {
        // Preveri, da so vsi podatki pravilni
        guard let earningsValue = Double(earnings), !company.isEmpty else {
            return // Prepreči shranjevanje, če manjkajo podatki
        }

        let newRecord = WorkRecord(context: viewContext)
        newRecord.company = company
        newRecord.earnings = earningsValue
        newRecord.startTime = startTime
        newRecord.endTime = endTime

        do {
            try viewContext.save()
        } catch {
            // Obvladuj napake
            print("Error saving work record: \(error.localizedDescription)")
        }
    }
}

struct AddWorkRecordView_Previews: PreviewProvider {
    static var previews: some View {
        AddWorkRecordView().environment(\.managedObjectContext, PersistenceController.preview.container.viewContext)
    }
}
