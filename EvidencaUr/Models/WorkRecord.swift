
import Foundation
import CoreData

@objc(WorkRecord)
public class WorkRecord: NSManagedObject {
    @NSManaged public var startTime: Date?
    @NSManaged public var endTime: Date?
    @NSManaged public var company: String?
    @NSManaged public var earnings: Double
}
