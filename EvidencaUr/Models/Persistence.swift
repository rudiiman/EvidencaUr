//
//  Untitled 2.swift
//  EvidencaUr
//
//  Created by Gašper Krajnc on 9. 6. 25.
//

import CoreData
import SwiftUI

class PersistenceController {
    static let shared = PersistenceController()

    // Seznam za povezavo z bazo
    static var preview: PersistenceController = {
        let result = PersistenceController(inMemory: true)
        let viewContext = result.container.viewContext
        // Tukaj lahko naložiš vzorčne podatke za testiranje
        return result
    }()

    let container: NSPersistentContainer

    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "EvidencaUr") // Uporabi ime projekta
        if inMemory {
            container.persistentStoreDescriptions.first?.url = URL(fileURLWithPath: "/dev/null")
        }
        container.loadPersistentStores { storeDescription, error in
            if let error = error as NSError? {
                fatalError("Unresolved error \(error), \(error.userInfo)")
            }
        }
    }

    // Funkcija za shranjevanje sprememb v bazi
    func saveContext () {
        let context = container.viewContext
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                let nserror = error as NSError
                fatalError("Unresolved error \(nserror), \(nserror.userInfo)")
            }
        }
    }
}
