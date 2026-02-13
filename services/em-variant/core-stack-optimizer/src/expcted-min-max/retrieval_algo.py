import sys

## find either the min or max value from a list of containers bay['stacks']
def getMinOrMaxStackCValue(findMax, stackContainers):
    res = None
    res_container = None
    if findMax:
        res = -1
        for container in stackContainers:
            if res < container[1]:
                res = container[1]
                res_container = container
    else:
        res = sys.maxsize
        for container in stackContainers:
            if res > container[1]:
                res = container[1]
                res_container = container
    return res, res_container

## maintain complete bay information list with below defined attributes
## this will iterate over complete bay and store necessary information
def createStackInfo(bay):
    stackInfo = []
    overAllMaxCValue = -1

    overAllMinCValue = sys.maxsize
    overAllMinContainer = None
    srcStack = None
    for item in bay.items():
        currStackInfo = {
            "stackName": item[0],
            "stackSize": len(item[1]),
            "items": item[1]
        }
        if len(item[1]) > 0:
            ## calculate max and min container values for the current stack
            currMaxCValue, currMaxContainer = getMinOrMaxStackCValue(True, item[1])
            currMinCValue, currMinContainer = getMinOrMaxStackCValue(False, item[1])
            currStackInfo.update({"maxStackCValue": currMaxCValue, "minStackCValue": currMinCValue})
            if overAllMaxCValue < currMaxCValue:
                overAllMaxCValue = currMaxCValue
            if overAllMinCValue > currMinCValue:
                overAllMinCValue = currMinCValue
                overAllMinContainer = currMinContainer
                srcStack = currStackInfo
        stackInfo.append(currStackInfo)

    ## setting up empty stacks min-max value
    for stack in stackInfo:
        if stack['stackSize'] == 0:
            stack.update({"maxStackCValue": overAllMaxCValue + 1, "minStackCValue": overAllMaxCValue + 1})
    return stackInfo, srcStack, overAllMinContainer


## find destination stack for a given container to be moved
def getDestinationStack(movingContainer, targetStacks, maxStackSize):

    probableStacks = []
    for stack in targetStacks:
        if stack["minStackCValue"] > movingContainer[1]:
            probableStacks.append(stack)

    if len(probableStacks) == 0:
        maxCValueStack = -1
        for stack in targetStacks:
            if stack['minStackCValue'] > maxCValueStack:
                maxCValueStack = stack['minStackCValue']

        for stack in targetStacks:
            if stack['minStackCValue'] == maxCValueStack:
                probableStacks.append(stack)

    destStack = None
    destStackCValue = sys.maxsize
    for stack in probableStacks:
        if stack["stackSize"] == maxStackSize - 1:
            continue
        if destStackCValue >= stack['minStackCValue']:
            if destStack is not None and destStack['minStackCValue'] == stack['minStackCValue'] and destStack['stackSize'] == stack['stackSize']:
                continue
            if destStack is not None and destStack['stackSize'] < stack['stackSize']:
                destStackCValue = stack['minStackCValue']
                destStack = stack
            else:
                destStackCValue = stack['minStackCValue']
                destStack = stack
    return destStack


def refereshTargetStackAttributes(targetStacks):
    for stack in targetStacks:
        stack.update({"stackSize": len(stack['items'])})
        if len(stack['items']) > 0:
            currMaxCValue, currMaxContainer = getMinOrMaxStackCValue(True, stack['items'])
            currMinCValue, currMinContainer = getMinOrMaxStackCValue(False, stack['items'])
            stack.update({"maxStackCValue": currMaxCValue, "minStackCValue": currMinCValue})


## to print the update bay after every step
def updated_bay(stackInfos):
    updated_bay = {}
    for stack in stackInfos:
        updated_bay[stack['stackName']] = stack['items']
    print("Updated Bay Configuration:")
    print(updated_bay)


def main():
    # bay2 = {
    #     'stack1': [('c1', 1), ('c2', 4), ('c3', 7), ('c4', 4), ('c5', 2)],
    #     'stack2': [('c6', 7), ('c7', 4)],
    #     'stack3': [('c10', 8)],
    #     'stack4': [('c8', 3), ('c9', 7)],
    #     'stack5': [],
    # }

    bay2 = {
        'stack1': [('c1', 1), ('c2', 4), ('c3', 7), ('c4', 4), ('c5', 2)],
        'stack2': [('c6', 7), ('c7', 4)],
        'stack3': [],
        'stack4': [('c8', 3), ('c9', 7)]
    }
    
    maxStackSize = 5
    while sum(len(stack) for stack in bay2.values()) > 0:

        overAllMaxCValue = max(prio for stack in bay2.values() for c_id, prio in stack)
        stackInfos, srcStack, srcContainer = createStackInfo(bay2)

        # Making target Stack list or s_prime list (stacks except source stacks from bay)
        targetStacks = []
        for stack in stackInfos:
            if stack['stackName'] == srcStack['stackName']:
                continue
            targetStacks.append(stack)

        iter = 1

        while len(srcStack['items']) != 0:
            movingContainer = srcStack['items'].pop()
            if movingContainer == srcContainer:
                print("Remove Final Source container:{} from Stack:{} ".format(srcContainer, srcStack["stackName"]))
                updated_bay(stackInfos)
                break
            destStack = getDestinationStack(movingContainer, targetStacks, maxStackSize)
            print("Moving container :{} from Source Stack: {} to Dest Stack: {}".format(movingContainer, srcStack["stackName"], destStack["stackName"]))
            
            destStack['items'].append(movingContainer)  ##add the container to the destination stack
            refereshTargetStackAttributes(targetStacks)

            iter+=1
            updated_bay(stackInfos)

        if len(srcStack['items']) > 0:
            ##remove the final container from the source stack
            srcStack['items'].pop()
            print("Final Source container:{} removed from Stack:{}".format(srcContainer, srcStack["stackName"]))
            updated_bay(stackInfos)
                
        srcStack['stackSize'] = 0
        srcStack['maxStackCValue'] = overAllMaxCValue + 1
        srcStack['minStackCValue'] = overAllMaxCValue + 1
        srcStack['items'] = []

        # print("Final source stack: ", srcStack)
        # update the initial bay configuration for the next iteration
        bay2 = {}
        for stack in stackInfos:
            bay2[stack['stackName']] = stack['items']

        updated_bay(stackInfos)

if __name__ == "__main__":
    main()
