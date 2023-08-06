# Pytorch Trainer

A library providing a simple trainer for pytorch models.  
It provides a similar interface to keras and aims to simplify development of models through providing metrics and callbacks.


# Example usage:
```python 
import pytorch_trainer
from pytorch_trainer import metrics
from pytorch_trainer import callbacks

model = MyModel()
loss_fn = MyLossFunction()
optimizer = MyOptimizer()

train_dataloader = MyTrainDataloader()
test_dataloader = MyTestDataloader()

trainer = pytorch_trainer.Trainer(model, loss_fn, optimizer, train_dataloader, test_dataloader,
                                  metrics=[metrics.BinaryAccuracy()],
                                  callbacks=[callbacks.EarlyStopping(monitor="test_binary_accuracy", patience=5, restore_weights=True),
                                             callbacks.TensorBoard()]
                                  )
trainer.train(epochs=20)
torch.save("my_best_model.pth", model.state_dict())
```