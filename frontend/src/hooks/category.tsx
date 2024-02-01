import { Page_CategoryOut_, CategoryOut, CategoryTypeEnum } from "sharkservers-sdk";


export default function useCategory(categories: Page_CategoryOut_ | undefined = undefined){

    const isApplicationCategory = (category: CategoryOut) => {
        return category.type == CategoryTypeEnum.APPLICATION
    }

    const isApplicationCategoryMany = (categoryId: number) => {
        let categoryObj: CategoryOut | undefined
        categories?.items.map((category, i) => {
            if (category.id === categoryId) {
                categoryObj = category
            }
        })
        if (!categoryObj) return false
        return isApplicationCategory(categoryObj)
    }

    

    return {
        isApplicationCategory: isApplicationCategory,
        isApplicationCategoryMany: isApplicationCategoryMany
    }
}